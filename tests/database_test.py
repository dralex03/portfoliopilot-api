from sqlalchemy.exc import NoResultFound
from src.database.connection import session, create_database
from src.database.models import Portfolio, PortfolioElement, User
from src.database.queries import insert_new_user


def test_model_creation():
    create_database()


def test_user_insertion():
    #  Test if the user insert_new_user function works and returns the right result
    user = insert_new_user('testuser@example.com', 'password')
    assert user is not None
    assert user.email == 'testuser@example.com'

    #  Test if User really is in database
    fetched_user = session.query(User).filter_by(email='testuser@example.com').first()
    print(f"Debug: Fetched user: {fetched_user}")
    assert fetched_user is not None
