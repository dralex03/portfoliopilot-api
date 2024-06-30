import pytest

from src.database.models import Base
from src.database.setup import Session, engine, initialize_default_data


@pytest.fixture(scope='function')
def session():
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
