from functools import wraps
from typing import Callable

from src.database.models import (Asset, AssetType, Portfolio, PortfolioElement,
                                 User)
from src.database.setup import session


def call_database_function(function: Callable):
    """
    Handles Errors for every query, in order to improve code quality by avoiding redundant try and except blocks
    Furthermore a commit after every transaction is ensured so inconsistencies are avoided
    In addition on error the database session gets rolled backed and in every case closed
        Parameters:
            Callable function;
        Returns:
            Any: The result of the passed function or the error with the name of the failed function;
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
            str email;
        Returns:
            User
    """
    return session.query(User).filter_by(email=email).first()


@call_database_function
def get_user_by_id(id: str):
    """
    Fetches a user by ID from the database
        Parameters:
            str id;
        Returns:
            User
    """
    return session.query(User).filter_by(id=id).one()


@call_database_function
def add_new_user(email: str, password: str):
    """
    Inserts new user into database and returns the created object
        Parameters:
            str email;
            str password;
        Returns:
            User
    """
    new_user = User(email=email, password=password)
    session.add(new_user)
    return new_user


# TODO: not used yet
@call_database_function
def delete_user_by_id(user_id: str):
    """
    Deletes a user based on the passed id
        Parameters:
            str user_id;
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
def add_portfolio(name: str, user_id: str):
    """
    Creates a portfolio based on the transferred name and ID of the user
        Parameters:
            str name;
            str user_id;
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
def get_portfolio_by_id(portfolio_id: str):
    """
    Fetches a portfolio by its ID.
        Parameters:
            str portfolio_id;
        Returns:
            Portfolio
    """
    return session.query(Portfolio).filter_by(id=portfolio_id).first()


@call_database_function
def get_portfolio_by_name(user_id: str, portfolio_name: str):
    """
    Fetches a portfolio by name for a specific user id
        Parameters:
            str portfolio_name;
        Returns:
            Portfolio
    """
    return session.query(Portfolio).filter_by(user_id=user_id, name=portfolio_name).first()


@call_database_function
def get_portfolios_by_user_id(user_id: str):
    """
    Fetches every portfolio that belongs to a specific user
        Parameters:
            str user_id;
        Returns:
            List[Portfolio]
    """
    return session.query(Portfolio).filter_by(user_id=user_id).all()


@call_database_function
def delete_portfolio_by_id(portfolio_id: str):
    """
    Deletes a portfolio based on the passed id
        Parameters:
            str portfolio_id;
        Returns:
            Boolean True if the Portfolio was successfully deleted, False otherwise
    """
    portfolio_to_delete = session.query(
        Portfolio).filter_by(id=portfolio_id).first()
    if portfolio_to_delete:
        session.delete(portfolio_to_delete)
        return True
    else:
        return False


@call_database_function
def update_portfolio_name(portfolio_id: str, new_portfolio_name: str):
    """
    Updates the name of a specific portfolio.
        Parameters:
            str portfolio_id;
            str new_portfolio_name;
        Returns:
            Portfolio
    """

    existing_portfolio = session.query(
        Portfolio).filter_by(id=portfolio_id).first()
    existing_portfolio.name = new_portfolio_name

    return existing_portfolio


@call_database_function
def add_portfolio_element(portfolio_id: str, asset_id: str, count: float, buy_price: float, order_fee: float):
    """
    Adds the passed portfolio element to the passed portfolio.
    If the portfolio already contains an element from that asset, the numbers are just updated.
        Parameters:
            str portfolio_id;
            str asset_id;
            float count;
            float buy_price;
            float order_fee;
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
def get_portfolio_element(portfolio_id: str, p_element_id: str):
    """
    Fetches a single PortfolioElement that belongs to a specific portfolio.
        Parameters:
            str portfolio_id;
            str p_element_id;
        Returns:
            PortfolioElement
    """
    return session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id, id=p_element_id).one()


# TODO: not used yet
@call_database_function
def get_portfolio_all_elements(portfolio_id: str):
    """
    Fetches every PortfolioElement that belongs to a user and portfolio.
        Parameters:
            str portfolio_id;
        Returns:
            List[PortfolioElement]
    """
    return session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id).all()


@call_database_function
def delete_portfolio_element(portfolio_id: str, p_element_id: str):
    """
    Deletes the portfolio element corresponding to the passed id and the portfolio ID.
        Parameters:
            str portfolio_id;
            str p_element_id;
        Returns:
            Boolean True if the portfolio element was successfully deleted, False otherwise
    """
    portfolio_element = session.query(PortfolioElement).filter_by(
        id=p_element_id, portfolio_id=portfolio_id).first()
    if portfolio_element:
        session.delete(portfolio_element)
        return True
    else:
        return False


@call_database_function
def update_portfolio_element(portfolio_id: str, p_element_id: str, count: float = None, buy_price: float = None,
                             order_fee: float = None):
    """
    Updates the details of a specific portfolio element
        Parameters:
            str portfolio_id;
            str p_element_id;
            float count;
            float buy_price;
            float order_fee;
        Returns:
            PortfolioElement
    """
    portfolio_element = session.query(PortfolioElement).filter_by(
        id=p_element_id, portfolio_id=portfolio_id).one()

    # Update count if existent and greater than 0, else delete the element
    if count is not None:
        if count > 0:
            portfolio_element.count = count
        else:
            session.delete(portfolio_element)
            return 'deleted'

    # Update buy price if existent
    if buy_price is not None and buy_price > 0:
        portfolio_element.buy_price = buy_price

    # Update order fee if existent
    if order_fee is not None and order_fee >= 0:
        portfolio_element.order_fee = order_fee

    return portfolio_element


@call_database_function
def add_new_asset(name: str, ticker_symbol: str, isin: str, default_currency: str, asset_type_id: str):
    """
    Creates an asset based on the transferred values
        Parameters:
            str name;
            str ticker_symbol;
            str isin;
            str default_currency;
            str asset_type_id;
        Returns:
            Asset
    """
    if session.query(AssetType).filter_by(id=asset_type_id).first():
        new_asset = Asset(name=name,
                          ticker_symbol=ticker_symbol,
                          isin=isin,
                          default_currency=default_currency,
                          asset_type_id=asset_type_id
                          )
        session.add(new_asset)
        return new_asset
    else:
        return None


# TODO: not used yet
@call_database_function
def get_asset_by_name(name: str):
    """
    Fetches an asset by name from the database
        Parameters:
            str name;
        Returns:
            Asset
    """
    return session.query(Asset).filter_by(name=name).one()


@call_database_function
def get_asset_by_ticker(ticker: str):
    """
    Fetches an asset by ticker from the database
        Parameters:
            str ticker;
        Returns:
            Asset
    """
    return session.query(Asset).filter_by(ticker_symbol=ticker).first()


# TODO: not used yet
@call_database_function
def delete_asset(asset_id: str):
    """
    Deletes an asset based on the passed id
        Parameters:
            str asset_id;
        Returns:
            Boolean True if the Asset was successfully deleted, False otherwise
    """
    target_asset = session.query(Asset).filter_by(id=asset_id).first()
    if target_asset:
        session.delete(target_asset)
        return True
    else:
        return False


# TODO: not used yet
@call_database_function
def add_new_asset_type(name: str, quote_type: str, unit_type: str):
    """
    Creates an asset_type based on the transferred values
        Parameters:
            str name;
            str quote_type;
            str unit_type;
        Returns:
            AssetType
    """
    new_asset_type = AssetType(
        name=name, quote_type=quote_type, unit_type=unit_type)
    session.add(new_asset_type)
    return new_asset_type


@call_database_function
def get_asset_type_by_quote_type(quote_type: str):
    """
    Fetches an asset_type by quote_type from the database
        Parameters:
            str quote_type;
        Returns:
           AssetType
    """
    return session.query(AssetType).filter_by(quote_type=quote_type).one()


# TODO: not used yet
@call_database_function
def delete_asset_type(asset_type_id: str):
    """
    Deletes an asset_type based on the passed id
        Parameters:
            str asset_type_id;
        Returns:
            Boolean True if the AssetType was successfully deleted, False otherwise
    """
    target_asset_type = session.query(
        AssetType).filter_by(id=asset_type_id).first()
    if target_asset_type:
        session.delete(target_asset_type)
        return True
    else:
        return False


@call_database_function
def get_ticker_symbols_of_portfolio(portfolio_id: int):
    """
    Fetches the ticker symbols associated with a specific portfolio
        Parameters:
            int portfolio_id
        Returns:
            List of tickers
    """

    tickers = [
        ticker_symbol for (ticker_symbol,) in (
            session.query(Asset.ticker_symbol)
            .join(PortfolioElement, PortfolioElement.asset_id == Asset.id)
            .filter(PortfolioElement.portfolio_id == portfolio_id)
            .all()
        )
    ]
    return tickers
