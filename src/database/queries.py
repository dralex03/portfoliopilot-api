from sqlalchemy.exc import NoResultFound
from src.database.models import Portfolio, PortfolioElement, User
from src.database.connection import database

session = database.get_session()


def add_portfolio(name, user_id):
    """
    Creates a portfolio based on the transferred name and ID of the user
        Parameters:
            str name
            int user_id
        Returns:
            Boolean: True if the portfolio was successfully created, else False
        Raises:
            Value Error: If name is not str or user_id not int
    """
    if not isinstance(name, str) or not isinstance(user_id, int):
        raise ValueError("Invalid input types for 'name' or 'user_id'.")

    try:
        new_portfolio = Portfolio(
            name=name,
            user_id=user_id,
        )
        session.add(new_portfolio)
        session.commit()
        return new_portfolio

    except Exception as e:
        session.rollback()
        print(f'Failed to add portfolio: {e}')
        return False


def delete_portfolio_by_id(portfolio_id):
    """
    Deletes a portfolio based on the passed id
        Parameters:
            int portfolio_id
        Returns:
            Boolean: True if the portfolio was successfully deleted, else False
        Raises:
            Value Error: If portfolio_id is not int
    """
    if not isinstance(portfolio_id, int):
        raise ValueError("Invalid input type for 'portfolio_id'")

    try:
        portfolio_to_delete = session.query(Portfolio).filter_by(id=portfolio_id).one()
        session.delete(portfolio_to_delete)
        session.commit()
        return True

    except NoResultFound:
        print(f'No portfolio found with id {portfolio_id}')
        return True

    except Exception as e:
        session.rollback()
        print(f'Failed to delete portfolio: {e}')
        return False


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
        Raises:
            Value Error: If portfolio_id, asset_id are not int and if count, buy_price or order_fee are not a Number
    """
    if not isinstance(portfolio_id, int) or not isinstance(asset_id, int) or not isinstance(count, float) \
            or not isinstance(buy_price, float) or not isinstance(order_fee, float):
        raise ValueError("Invalid input types for 'portfolio_id', 'asset_id', 'count', 'buy_price' or 'order_fee'.")

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

    try:
        portfolio_element = PortfolioElement(count=count, buy_price=buy_price, order_fee=order_fee,
                                             portfolio_id=portfolio_id, asset_id=asset_id)
        session.add(portfolio_element)
        session.commit()
        return portfolio_element
    except Exception as e:
        session.rollback()
        print(f'Failed to insert asset: {e}')
        return False


def remove_portfolio_element(portfolio_id, asset_id):
    """
    Deletes a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count (optional)
        Returns:
            Boolean: True if the portfolio element was successfully deleted or reduced, else False
        Raises:
            Value Error: If portfolio_id or asset_id are not int
    """
    if not isinstance(portfolio_id, int) or not isinstance(asset_id, int):
        raise ValueError("Invalid input types for 'portfolio_id', 'asset_id' or 'count'.")

    try:
        target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                             asset_id=asset_id).one()
        session.delete(target_portfolio_element)
        session.commit()
        return True

    except NoResultFound:
        print(f'No PortfolioElement found with portfolio_id {portfolio_id} and asset_id {asset_id}')
        return True
    except Exception as e:
        session.rollback()
        print(f'Failed to delete PortfolioElement: {e}')
        return False


def reduce_portfolio_element(portfolio_id, asset_id, count):
    """
    Reduces the count of a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count (optional)
        Returns:
            Boolean: True if the portfolio element was successfully deleted or reduced, else False
        Raises:
            Value Error: If portfolio_id or asset_id are not int
    """
    if not isinstance(portfolio_id, int) or not isinstance(asset_id, int) or not isinstance(count, float):
        raise ValueError("Invalid input types for 'portfolio_id', 'asset_id' or 'count'.")

    try:
        target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                             asset_id=asset_id).one()
        if 0 < count < target_portfolio_element.count:
            target_portfolio_element.count = target_portfolio_element.count - count
        else:
            session.delete(target_portfolio_element)
        session.commit()
        return target_portfolio_element

    except NoResultFound:
        print(f'No PortfolioElement found with portfolio_id {portfolio_id} and asset_id {asset_id}')
        return True
    except Exception as e:
        session.rollback()
        print(f'Failed to delete PortfolioElement: {e}')
        return False


def get_user_by_email(email):
    """
    Fetches a user by email from the database
        Parameters:
            email: str
        Returns:
            User: user object
        Raises:
            Value Error: If email is not str
    """
    if not isinstance(email, str):
        raise ValueError("Invalid input type for 'email'.")

    return session.query(User).filter(User.email == email).first()


def insert_new_user(email, password):
    """
    Inserts new user into database and returns the created object
        Parameters:
            email: str
            password: str
        Returns:
            User: created user object
        Raises:
            Value Error: If email or password are not str
    """
    if not isinstance(email, str) or not isinstance(password, str):
        raise ValueError("Invalid input types for 'email' or 'password'.")

    try:
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        print(f'Failed to insert User: {e}')
        session.rollback()
        return None
