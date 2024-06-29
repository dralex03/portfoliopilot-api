import pytest

from flask.testing import FlaskClient

from src import create_app
from src.database.setup import engine, Session, initialize_default_data
from src.database.models import Base


@pytest.fixture(scope='module')
def setup_session():
    """
    Pytest Fixture that sets up a database session for API Tests.
        Parameters:
            -
        Returns:
            -
    """
    # Check for SQLite for test environment
    if not engine.url.get_backend_name() == 'sqlite':
        raise RuntimeError('Use SQLite Database to run tests')
    
    Base.metadata.create_all(engine)
    initialize_default_data()
    try:
        # Creates a session and gives it to the testing function
        with Session() as session:
            yield session
    finally:
        # Cleans up database after tests have run
        Base.metadata.drop_all(engine)


@pytest.fixture(scope='module')
def test_client(setup_session):
    """
    Pytest fixture that sets up a flask app and a test client for testing API requests.
        Parameters:
            Session setup_session;
        Returns:
            -
    """
    flask_app: FlaskClient = create_app()
    flask_app.config.update({
        'TESTING': True,
    })

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client