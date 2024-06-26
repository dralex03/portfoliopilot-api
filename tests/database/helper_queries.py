

from src.database.queries import *

def insert_new_user(name: str):
    new_user = User(email=name, password=name)
    session.add(new_user)
    session.commit()
    return new_user


def insert_new_portfolio(name: str, user_id: str):
    new_portfolio = Portfolio(name=name, user_id=user_id)
    session.add(new_portfolio)
    session.commit()
    return new_portfolio


def insert_new_portfolio_element(value: float, portfolio_id: str, asset_id: str):
    new_portfolio_element = PortfolioElement(portfolio_id=portfolio_id, asset_id=asset_id, count=value,
                                             buy_price=value, order_fee=value)
    session.add(new_portfolio_element)
    session.commit()
    return new_portfolio_element


def insert_new_asset(name: str, asset_type_id: str):
    new_asset = Asset(name=name, ticker_symbol=name, isin=name, default_currency=name,
                      asset_type_id=asset_type_id)
    session.add(new_asset)
    session.commit()
    return new_asset


def insert_new_asset_type(name: str):
    new_asset_type = AssetType(name=name, unit_type=name)
    session.add(new_asset_type)
    session.commit()
    return new_asset_type