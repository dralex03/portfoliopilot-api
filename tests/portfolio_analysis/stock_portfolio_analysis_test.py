import pytest
from src.database.setup import engine
from src.database.models import Base
from src.portfolio_analysis.stock_analysis import *
from tests.database_testing_functions import *


def test_get_stock_portfolio_distribution():
    NAME = 'TGSPD'
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)
    new_asset_type = insert_new_asset_type('stock')

    #  Technology / United States
    apple_stock = insert_new_asset('AAPL', new_asset_type.id)
    insert_new_portfolio_element(10.0, new_portfolio.id, apple_stock.id)

    #  Technology / Germany
    sap_stock = insert_new_asset('SAP', new_asset_type.id)
    insert_new_portfolio_element(10.0, new_portfolio.id, sap_stock.id)

    #  Consumer Cyclical / China
    alibaba_stock = insert_new_asset('BABA', new_asset_type.id)
    insert_new_portfolio_element(10.0, new_portfolio.id, alibaba_stock.id)

    test_country_weightings, test_sector_weightings = get_stock_portfolio_distribution(new_portfolio.id)

    assert len(test_country_weightings) == 3
    assert len(test_sector_weightings) == 2

    assert test_country_weightings['United States'] == 33.33
    assert test_country_weightings['Germany'] == 33.33
    assert test_country_weightings['China'] == 33.33

    assert test_sector_weightings['Technology'] == 66.67
    assert test_sector_weightings['Consumer Cyclical'] == 33.33

