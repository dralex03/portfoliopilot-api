from src.database import models
from src.database.connection import session

def get_user_by_email(email: str):
    """
    Fetches a user by email from the database
        Parameters:
            str email;
        Returns:
            User: user object
    """

    return session.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(id: int):
    """
    Fetches a user by ID from the database
        Parameters:
            int id;
        Returns:
            User: user object
    """

    return session.query(models.User).filter(models.User.id == id).one()

def insert_new_user(email: str, password: str):
    """
    Inserts new user into database and returns the created object
        Parameters:
            str email;
            str password;
        Returns:
            User: newly created user object
    """

    try:
        new_user = models.User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        print('Error inserting new user: ' + e)
        return None