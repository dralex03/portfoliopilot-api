from src.database import models
from src.database.connection import session

def get_user_by_email(email):
    """
    Fetches a user by email from the database
        Parameters:
            email: str
        Returns:
            User: user object
    """

    return session.query(models.User).filter(models.User.email == email).first()

def insert_new_user(email, password):
    """
    Inserts new user into database and returns the created object
        Parameters:
            email: str
            password: str
        Returns:
            User: created user object
    """

    try:
        new_user = models.User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        print('Error inserting new user: ' + e)
        return None