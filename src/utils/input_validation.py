import re
from src import config

def is_valid_email(email):
    """
    Checks a string if it's a valid email address.
        Parameters:
            email: str
        Returns:
            bool: Whether the email parameter is a valid email or not.
    """

    # Regular expression for email addresses
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    return re.match(email_regex, email) is not None

def is_strong_password(password):
    """
    Checks if a password fulfills the password requirements:
    - minimum length 8 characters
    - includes upper and lower case letters
    - at least one number
    - at least one special character

        Parameters:
            password: str
        Returns:
            bool: If the password meets the requirements
    """

    # Check minimum length
    if len(password) < config.MINIMUM_PASSWORD_LEN:
        return False

    # Checks for upper case, lower case, numbers and special characters
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>+-]', password):
        return False

    return True
