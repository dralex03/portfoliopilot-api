import pytest
from src.database.setup import engine, Session
from src.database.models import Base

@pytest.fixture(scope='function')
def session():
    # Check for SQLite for test environment
    if not engine.url.get_backend_name() == 'sqlite':
        raise RuntimeError('Use SQLite Database to run tests')
    
    Base.metadata.create_all(engine)
    try:
        # Creates a session and gives it to the testing function
        with Session() as session:
            yield session
    finally:
        # Cleans up database after tests have run
        Base.metadata.drop_all(engine)
