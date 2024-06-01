from sqlalchemy.exc import NoResultFound
from src.database.database_models import Portfolio, PortfolioElement, User
from src.database.database import database

session = database.get_session()


def add_portfolio(name, user_id):
    """
    Creates a portfolio based on the transferred name and ID of the user
        Parameters:
            str name
            int user_id
        Returns:
            Boolean: True if the portfolio was successfully created, else False
    """

    new_portfolio = Portfolio(
        name=name,
        user_id=user_id,
    )
    session.add(new_portfolio)
    session.commit()
    return new_portfolio


def delete_portfolio_by_id(portfolio_id):
    """
    Deletes a portfolio based on the passed id
        Parameters:
            int portfolio_id
        Returns:
            Boolean: True if the portfolio was successfully deleted, else False
    """
    portfolio_to_delete = session.query(Portfolio).filter_by(id=portfolio_id).one()
    session.delete(portfolio_to_delete)
    session.commit()
    return True


def insert_portfolio_element(portfolio_id, asset_id, count, buy_price, order_fee):
    """
    Adds the transferred portfolio element to the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count
            float buy_price
            float order_fee
        Returns:
            Boolean: True if the portfolio element was successfully added, else False
    """
    existing_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                 asset_id=asset_id).first()
    if existing_element:
        existing_element_total_buy_price = existing_element.buy_price * existing_element.count
        new_element_total_buy_price = buy_price * count
        combined_element_count = count + existing_element.count
        existing_element.buy_price = ((existing_element_total_buy_price +
                                       new_element_total_buy_price) / combined_element_count)
        existing_element.order_fee += order_fee
        existing_element.count += count
        session.commit()
        return existing_element

    portfolio_element = PortfolioElement(count=count, buy_price=buy_price, order_fee=order_fee,
                                         portfolio_id=portfolio_id, asset_id=asset_id)
    session.add(portfolio_element)
    session.commit()
    return portfolio_element


def delete_portfolio_element(portfolio_id, asset_id):
    """
    Deletes a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count (optional)
        Returns:
            Boolean: True if the portfolio element was successfully deleted or reduced, else False
    """
    target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                         asset_id=asset_id).one()
    session.delete(target_portfolio_element)
    session.commit()
    return True


def reduce_portfolio_element(portfolio_id, asset_id, count):
    """
    Reduces the count of a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count (optional)
        Returns:
            Boolean: True if the portfolio element was successfully deleted or reduced, else False
    """
    target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                         asset_id=asset_id).one()
    if 0 < count < target_portfolio_element.count:
        target_portfolio_element.count = target_portfolio_element.count - count
    else:
        session.delete(target_portfolio_element)
    session.commit()
    return target_portfolio_element


def get_user_by_email(email):
    """
    Fetches a user by email from the database
        Parameters:
            email: str
        Returns:
            User: user object
    """
    return session.query(User).filter(User.email == email).first()


def insert_new_user(email, password):
    """
    Inserts new user into database and returns the created object
        Parameters:
            email: str
            password: str
        Returns:
            User: created user object
    """
    new_user = User(email=email, password=password)
    session.add(new_user)
    session.commit()
    return new_user


def call_database_function(function, *args):
    """
        Handles Errors for every query, in order to improve code quality by avoiding redundant try and except blocks
        Furthermore a commit after every transaction is ensured so inconsistencies are avoided
        In addition on error the database session gets rolled backed and in every case closed
    Args:
        function:
        *args:

    Returns:
        The result of the passed function or the error with the name of the failed function
    """
    try:
        result = function(*args)
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        function_name = function.__name__
        print(f'Error in function {function_name}: {e}')
        raise

