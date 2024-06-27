import string
import random

from src.database.queries import *


def generate_random_email(n=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n)) + '@example.com'


def generate_random_string(n=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def generate_random_float():
    return round(random.uniform(0, 100), 2)


def generate_new_asset_type():
    ASSET_TYPE_NAME = generate_random_string()
    QUOTE_TYPE = generate_random_string()
    UNIT_TYPE = generate_random_string()
    return insert_new_asset_type(ASSET_TYPE_NAME, QUOTE_TYPE, UNIT_TYPE)


def generate_new_asset(asset_type_id):
    ASSET_NAME = generate_random_string()
    TICKER_SYMBOL = generate_random_string()
    ISIN = generate_random_string()
    DEFAULT_CURRENCY = generate_random_string()
    return insert_new_asset(ASSET_NAME, TICKER_SYMBOL, ISIN, DEFAULT_CURRENCY, asset_type_id)


def generate_new_user():
    USER_NAME = generate_random_string()
    EMAIL = generate_random_email()
    return insert_new_user(EMAIL, USER_NAME)


def generate_new_portfolio(user_id):
    PORTFOLIO_NAME = generate_random_string()
    return insert_new_portfolio(PORTFOLIO_NAME, user_id)


def generate_new_portfolio_element(portfolio_id: str, asset_id: str):
    COUNT = generate_random_float()
    BUY_PRICE = generate_random_float()
    ORDER_FEE = generate_random_float()
    return add_portfolio_element(portfolio_id, asset_id, COUNT, BUY_PRICE, ORDER_FEE)


def insert_new_user(email: str, name: str):
    new_user = User(email=email, password=name)
    session.add(new_user)
    session.commit()
    return new_user


def insert_new_portfolio(name: str, user_id: str):
    new_portfolio = Portfolio(name=name, user_id=user_id)
    session.add(new_portfolio)
    session.commit()
    return new_portfolio


def insert_new_portfolio_element(portfolio_id: str, asset_id: str, count: float, buy_price: float, order_fee: float):
    new_portfolio_element = PortfolioElement(portfolio_id=portfolio_id, asset_id=asset_id, count=count,
                                             buy_price=buy_price, order_fee=order_fee)
    session.add(new_portfolio_element)
    session.commit()
    return new_portfolio_element


def insert_new_asset(name: str, ticker_symbol: str, isin: str, default_currency: str, asset_type_id: str):
    new_asset = Asset(name=name, ticker_symbol=ticker_symbol, isin=isin, default_currency=default_currency,
                      asset_type_id=asset_type_id)
    session.add(new_asset)
    session.commit()
    return new_asset


def insert_new_asset_type(name: str, quote_type: str, unit_type: str):
    new_asset_type = AssetType(name=name, quote_type=quote_type, unit_type=unit_type)
    session.add(new_asset_type)
    session.commit()
    return new_asset_type
