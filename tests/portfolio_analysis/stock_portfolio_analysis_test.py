import pytest

from sqlalchemy.orm.session import Session

from src.portfolio_analysis.stock_analysis import *

from tests.database.helper_queries import *
from tests.database.conftest import session


def test_get_stock_portfolio_distribution(session: Session):
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_asset_type = generate_new_asset_type()

    #  Technology / United States
    name = 'Apple'
    ticker_symbol = 'AAPL'
    isin = generate_random_string()
    default_currency = generate_random_string()

    new_asset = insert_new_asset(name, ticker_symbol, isin, default_currency, new_asset_type.id)

    count = generate_random_float()
    buy_price = generate_random_float()
    order_fee = generate_random_float()
    insert_new_portfolio_element(new_portfolio.id, new_asset.id, count, buy_price, order_fee)

    #  Technology / Germany
    name = 'SAP'
    ticker_symbol = 'SAP'
    isin = generate_random_string()
    default_currency = generate_random_string()

    new_asset = insert_new_asset(name, ticker_symbol, isin, default_currency, new_asset_type.id)

    count = generate_random_float()
    buy_price = generate_random_float()
    order_fee = generate_random_float()
    insert_new_portfolio_element(new_portfolio.id, new_asset.id, count, buy_price, order_fee)

    #  Consumer Cyclical / China
    name = 'Alibaba'
    ticker_symbol = 'BABA'
    isin = generate_random_string()
    default_currency = generate_random_string()

    new_asset = insert_new_asset(name, ticker_symbol, isin, default_currency, new_asset_type.id)

    count = generate_random_float()
    buy_price = generate_random_float()
    order_fee = generate_random_float()
    insert_new_portfolio_element(new_portfolio.id, new_asset.id, count, buy_price, order_fee)

    test_country_weightings, test_sector_weightings, test_trailing_pe = (
        get_stock_portfolio_distribution(new_portfolio.id))

    assert len(test_country_weightings) == 3
    assert len(test_sector_weightings) == 2

    assert test_country_weightings['United States'] == 33.33
    assert test_country_weightings['Germany'] == 33.33
    assert test_country_weightings['China'] == 33.33

    assert test_sector_weightings['Technology'] == 66.67
    assert test_sector_weightings['Consumer Cyclical'] == 33.33
