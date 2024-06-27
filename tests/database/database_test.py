import pytest
from sqlalchemy.orm.session import Session

from src.database.queries import *
from src.database.models import *

from tests.database.conftest import session
from tests.database.helper_queries import *


def test_user_insertion(session: Session):
    new_user = generate_new_user()

    fetched_user = session.query(User).filter_by(email=new_user.email).first()

    assert fetched_user is not None
    assert fetched_user.email == new_user.email

    with pytest.raises(Exception):
        add_new_user(new_user.email, new_user.password)


def test_user_deletion(session: Session):
    new_user = generate_new_user()

    delete_user_by_id(new_user.id)

    fetched_user = session.query(User).filter_by(email=new_user.email).first()
    assert fetched_user is None


def test_get_user_by_email(session: Session):
    new_user = generate_new_user()

    user = get_user_by_email(new_user.email)
    assert user is not None
    assert user.email == new_user.email

    fake_mail = '1234'  # @example.com is always missing here and therefore it cant be the real mail by coincidence
    user = get_user_by_email(fake_mail)
    assert user is None


def test_get_user_by_id(session: Session):
    new_user = generate_new_user()

    user = get_user_by_id(new_user.id)

    assert user is not None
    assert user.id == new_user.id


def test_portfolio_insertion(session: Session):
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    fetched_portfolio = session.query(Portfolio).filter_by(name=new_portfolio.name, user_id=new_user.id).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == new_portfolio.name
    assert fetched_portfolio.user_id == new_user.id


def test_portfolio_element_insertion(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    COUNT = generate_random_float()
    BUY_PRICE = generate_random_float()
    ORDER_FEE = generate_random_float()
    add_portfolio_element(new_portfolio.id, new_asset.id, COUNT, BUY_PRICE, ORDER_FEE)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                          asset_id=new_asset.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == COUNT
    assert fetched_portfolio_element.buy_price == BUY_PRICE
    assert fetched_portfolio_element.order_fee == ORDER_FEE


def test_portfolio_element_update(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_portfolio_element = generate_new_portfolio_element(new_portfolio.id, new_asset.id)

    COUNT = generate_random_float()
    BUY_PRICE = generate_random_float()
    ORDER_FEE = generate_random_float()
    update_portfolio_element(new_portfolio.id, new_portfolio_element.id, COUNT, BUY_PRICE, ORDER_FEE)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == COUNT


def test_get_portfolio_element(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_portfolio_element = generate_new_portfolio_element(new_portfolio.id, new_asset.id)

    fetched_portfolio_element = get_portfolio_element(new_portfolio.id, new_portfolio_element.id)

    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.count == new_portfolio_element.count
    assert fetched_portfolio_element.order_fee == new_portfolio_element.order_fee
    assert fetched_portfolio_element.buy_price == new_portfolio_element.buy_price


def test_get_portfolio_all_elements(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset_type_2 = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_asset_2 = generate_new_asset(new_asset_type_2.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_portfolio_element = generate_new_portfolio_element(new_portfolio.id, new_asset.id)
    new_portfolio_element_2 = generate_new_portfolio_element(new_portfolio.id, new_asset_2.id)

    fetched_portfolio_elements = get_portfolio_all_elements(new_portfolio.id)

    assert fetched_portfolio_elements is not None
    assert len(fetched_portfolio_elements) == 2
    assert any(portfolio.order_fee == new_portfolio_element.order_fee for portfolio in fetched_portfolio_elements)
    assert any(portfolio.order_fee == new_portfolio_element_2.order_fee for portfolio in fetched_portfolio_elements)
    assert any(portfolio.count == new_portfolio_element.count for portfolio in fetched_portfolio_elements)
    assert any(portfolio.count == new_portfolio_element_2.count for portfolio in fetched_portfolio_elements)
    assert any(portfolio.buy_price == new_portfolio_element.buy_price for portfolio in fetched_portfolio_elements)
    assert any(portfolio.buy_price == new_portfolio_element_2.buy_price for portfolio in fetched_portfolio_elements)


def test_portfolio_element_deletion(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_portfolio_element = generate_new_portfolio_element(new_portfolio.id, new_asset.id)

    delete_portfolio_element(new_portfolio.id, new_portfolio_element.id)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                          asset_id=new_asset.id).first()
    assert fetched_portfolio_element is None


def test_get_portfolio_by_user_id(session: Session):
    new_user = generate_new_user()
    portfolio1 = generate_new_portfolio(new_user.id)
    portfolio2 = generate_new_portfolio(new_user.id)

    fetched_portfolio_user_id = get_portfolios_by_user_id(new_user.id)
    assert fetched_portfolio_user_id is not None
    assert len(fetched_portfolio_user_id) == 2
    assert any(portfolio.name == portfolio1.name for portfolio in fetched_portfolio_user_id)
    assert any(portfolio.name == portfolio2.name for portfolio in fetched_portfolio_user_id)


def test_get_portfolio_by_id(session: Session):
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    fetched_portfolio_by_id = get_portfolio_by_id(new_portfolio.id)
    assert fetched_portfolio_by_id is not None
    assert fetched_portfolio_by_id.name == new_portfolio.name


def test_get_portfolio_by_name(session: Session):
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    fetched_portfolio_by_name = get_portfolio_by_name(new_user.id, new_portfolio.name)
    assert fetched_portfolio_by_name is not None
    assert fetched_portfolio_by_name.name == new_portfolio.name


def test_update_portfolio_name(session: Session):
    NEW_NAME = generate_random_string()
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    updated_portfolio = update_portfolio_name(new_portfolio.id, NEW_NAME)
    assert updated_portfolio is not None
    assert updated_portfolio.name == NEW_NAME


def test_portfolio_deletion(session: Session):
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)

    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)
    new_user = generate_new_user()
    new_portfolio = generate_new_portfolio(new_user.id)
    new_portfolio_element = generate_new_portfolio_element(new_portfolio.id, new_asset.id)

    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is None

    fetched_asset = session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None

    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()
    assert fetched_asset_type is not None


def test_asset_insertion(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)

    fetched_asset = session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_get_asset_by_name(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)

    fetched_asset = get_asset_by_name(new_asset.name)

    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_get_asset_by_ticker(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)

    fetched_asset = get_asset_by_ticker(new_asset.ticker_symbol)

    assert fetched_asset is not None
    assert fetched_asset.ticker_symbol == new_asset.ticker_symbol


def test_asset_deletion(session: Session):
    new_asset_type = generate_new_asset_type()
    new_asset = generate_new_asset(new_asset_type.id)

    delete_asset(new_asset.id)

    with pytest.raises(Exception):
        get_asset_by_name(new_asset.name)


def test_asset_type_insertion(session: Session):
    new_asset_type = generate_new_asset_type()

    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name

    with pytest.raises(Exception):
        add_new_asset_type(new_asset_type.name, new_asset_type.quote_type, new_asset_type.unit_type)


def test_get_asset_type_by_name(session: Session):
    new_asset_type = generate_new_asset_type()

    fetched_asset_type = get_asset_type_by_quote_type(new_asset_type.quote_type)

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name


def test_asset_type_deletion(session: Session):
    new_asset_type = generate_new_asset_type()

    delete_asset_type(new_asset_type.id)
    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is None
