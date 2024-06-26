from functools import wraps
from src.database.models import Portfolio, PortfolioElement, User, Asset, AssetType
from src.database.setup import session
from typing import Callable


def call_database_function(function: Callable):
    """
        Handles Errors for every query, in order to improve code quality by avoiding redundant try and except blocks
        Furthermore a commit after every transaction is ensured so inconsistencies are avoided
        In addition on error the database session gets rolled backed and in every case closed
    Args:
        Callable function
    Returns:
        The result of the passed function or the error with the name of the failed function
    """

    @wraps(function)
    def wrapper(*args: any, **kwargs: any):
        try:
            result = function(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e

    return wrapper


@call_database_function
def get_user_by_email(email: str):
    """
    Fetches a user by email from the database
        Parameters:
            str email
        Returns:
            User
    """
    return session.query(User).filter_by(email=email).first()


@call_database_function
def get_user_by_id(id: int):
    """
    Fetches a user by ID from the database
        Parameters:
            int id
        Returns:
            User
    """
    return session.query(User).filter_by(id=id).one()


@call_database_function
def add_new_user(email: str, password: str):
    """
    Inserts new user into database and returns the created object
        Parameters:
            str email
            str password
        Returns:
            User
    """
    new_user = User(email=email, password=password)
    session.add(new_user)
    return new_user


@call_database_function
def delete_user_by_id(user_id: int):
    """
    Deletes a user based on the passed id
        Parameters:
            int user_id
        Returns:
            Boolean True if the user was successfully deleted, False otherwise
    """
    user_to_delete = session.query(User).filter_by(id=user_id).first()
    if user_to_delete:
        session.delete(user_to_delete)
        return True
    else:
        return False


@call_database_function
def add_portfolio(name: str, user_id: int):
    """
    Creates a portfolio based on the transferred name and ID of the user
        Parameters:
            str name
            int user_id
        Returns:
            Portfolio
    """
    new_portfolio = Portfolio(
        name=name,
        user_id=user_id,
    )
    session.add(new_portfolio)
    return new_portfolio


@call_database_function
def get_portfolio_by_user_id(user_id: int):
    """
    Fetches every portfolio that belongs to a specific user
        Parameters:
            int user_id
        Returns:
            List[Portfolio]
    """
    return session.query(Portfolio).filter_by(user_id=user_id).all()


@call_database_function
def delete_portfolio_by_id(portfolio_id: int):
    """
    Deletes a portfolio based on the passed id
        Parameters:
            int portfolio_id
        Returns:
            Boolean True if the Portfolio was successfully deleted, False otherwise
    """
    portfolio_to_delete = session.query(Portfolio).filter_by(id=portfolio_id).first()
    if portfolio_to_delete:
        session.delete(portfolio_to_delete)
        return True
    else:
        return False


@call_database_function
def add_portfolio_element(portfolio_id: int, asset_id: int, count: float, buy_price: float, order_fee: float):
    """
    Adds the passed portfolio element to the passed portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count
            float buy_price
            float order_fee
        Returns:
            PortfolioElement
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
        return existing_element

    portfolio_element = PortfolioElement(count=count, buy_price=buy_price, order_fee=order_fee,
                                         portfolio_id=portfolio_id, asset_id=asset_id)
    session.add(portfolio_element)
    return portfolio_element


@call_database_function
def get_portfolio_element(portfolio_id: int):
    """
    Fetches every PortfolioElement that belongs to a user and portfolio.
        Parameters:
            int portfolio_id
            int user_id
        Returns:
            List[PortfolioElement]
    """
    return session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id).all()


@call_database_function
def delete_portfolio_element(portfolio_element_id: int):
    """
    Deletes the portfolio element corresponding to the passed id
        Parameters:
            int portfolio_element_id
        Returns:
            Boolean True if the Portfolio_element was successfully deleted, False otherwise
    """
    target_portfolio_element = session.query(PortfolioElement).filter_by(id=portfolio_element_id).first()
    if target_portfolio_element:
        session.delete(target_portfolio_element)
        return False
    else:
        return False


@call_database_function
def reduce_portfolio_element(portfolio_id: int, asset_id: int, count: float):
    """
    Reduces the count of a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            float count
        Returns:
            PortfolioElement
    """
    target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                         asset_id=asset_id).one()
    if 0 < count < target_portfolio_element.count:
        target_portfolio_element.count = target_portfolio_element.count - count
    else:
        session.delete(target_portfolio_element)
    return target_portfolio_element


@call_database_function
def add_new_asset(name: str, ticker_symbol: str, isin: str, default_currency: str, asset_type_id: int):
    """
    Creates an asset based on the transferred values
        Parameters:
            str name
            str ticker_symbol
            str isin
            str default_currency
            int asset_type_id
        Returns:
            Asset
    """
    if session.query(AssetType).filter_by(id=asset_type_id).first():
        new_asset = Asset(name=name, ticker_symbol=ticker_symbol, isin=isin, default_currency=default_currency,
                          asset_type_id=asset_type_id)
        session.add(new_asset)
        return new_asset
    else:
        return None


@call_database_function
def get_asset_by_name(name: str):
    """
    Fetches an asset by name the database
        Parameters:
            str name
        Returns:
            Asset
    """
    return session.query(Asset).filter_by(name=name).one()


@call_database_function
def delete_asset(asset_id: int):
    """
    Deletes an asset based on the passed id
        Parameters:
            int asset_id
        Returns:
            Boolean True if the Asset was successfully deleted, False otherwise
    """
    target_asset = session.query(Asset).filter_by(asset_type_id=asset_id).first()
    if target_asset:
        session.delete(target_asset)
        return True
    else:
        return False


@call_database_function
def add_new_asset_type(name: str, unit_type: str):
    """
    Creates an asset_type based on the transferred values
        Parameters:
            str name
            str unit_type
        Returns:
            AssetType
    """
    new_asset_type = AssetType(name=name, unit_type=unit_type)
    session.add(new_asset_type)
    return new_asset_type


@call_database_function
def get_asset_type_by_name(name: str):
    """
    Fetches an asset_type by name the database
        Parameters:
            str name
        Returns:
           AssetType
    """
    return session.query(AssetType).filter_by(name=name).one()


@call_database_function
def delete_asset_type(asset_type_id: int):
    """
    Deletes an asset_type based on the passed id
        Parameters:
            int asset_type_id
        Returns:
            Boolean True if the AssetType was successfully deleted, False otherwise
    """
    target_asset_type = session.query(AssetType).filter_by(id=asset_type_id).first()
    if target_asset_type:
        session.delete(target_asset_type)
        return True
    else:
        return False
