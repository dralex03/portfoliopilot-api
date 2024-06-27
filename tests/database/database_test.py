import pytest
from sqlalchemy.orm.session import Session

from src.database.queries import *
from src.database.models import *

from tests.database.conftest import session
from tests.database.helper_queries import *


def test_user_insertion(session: Session):
    USER_EMAIL = 'UR@example.com'
    PASSWORD = '<PASSWORD>'
    add_new_user(USER_EMAIL, PASSWORD)

    fetched_user = session.query(User).filter_by(email=USER_EMAIL).first()

    assert fetched_user is not None
    assert fetched_user.email == USER_EMAIL

    with pytest.raises(Exception):
        add_new_user(USER_EMAIL, PASSWORD)


def test_user_deletion(session: Session):
    new_user = insert_new_user('UD')

    delete_user_by_id(new_user.id)

    fetched_user = session.query(User).filter_by(email=new_user.email).first()
    assert fetched_user is None


def test_get_user_by_email(session: Session):
    new_user = insert_new_user('TGUBE')

    user = get_user_by_email(new_user.email)
    assert user is not None
    assert user.email == new_user.email

    user = get_user_by_email('d!3d?4#cDcBAD3')
    assert user is None


def test_get_user_by_id(session: Session):
    new_user = insert_new_user('TGUBE')

    user = get_user_by_id(new_user.id)

    assert user is not None
    assert user.id == new_user.id


def test_portfolio_insertion(session: Session):
    new_user = insert_new_user('TPI')

    PORTFOLIO_NAME = 'Welt portfolio'
    add_portfolio(PORTFOLIO_NAME, new_user.id)

    fetched_portfolio = session.query(Portfolio).filter_by(name=PORTFOLIO_NAME, user_id=new_user.id).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == PORTFOLIO_NAME
    assert fetched_portfolio.user_id == new_user.id


def test_portfolio_element_insertion(session: Session):
    NAME = 'TPEI'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)

    add_portfolio_element(new_portfolio.id, new_asset.id, 10.0, 10.0, 10.0)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                          asset_id=new_asset.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.order_fee == 10.0
    assert fetched_portfolio_element.buy_price == 10.0
    assert fetched_portfolio_element.order_fee == 10.0


def test_portfolio_element_update(session: Session):
    NAME = 'TPER'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)
    new_portfolio_element = insert_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    update_portfolio_element(new_portfolio.id, new_portfolio_element.id, 5.0)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == 5.0


def test_get_portfolio_element(session: Session):
    FIRST_NAME = 'TGPE'
    new_asset_type = insert_new_asset_type(FIRST_NAME)
    new_asset_1 = insert_new_asset(FIRST_NAME, new_asset_type.id)
    new_user = insert_new_user(FIRST_NAME)
    new_portfolio = insert_new_portfolio(FIRST_NAME, new_user.id)
    new_portfolio_element = insert_new_portfolio_element(10.0, new_portfolio.id, new_asset_1.id)

    fetched_portfolio_element = get_portfolio_element(new_portfolio.id, new_portfolio_element.id)

    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.order_fee == 10.0


def test_get_portfolio_all_elements(session: Session):
    FIRST_NAME = 'TGP1'
    SECOND_NAME = 'TGP2'

    new_asset_type = insert_new_asset_type(FIRST_NAME)
    new_asset_1 = insert_new_asset(FIRST_NAME, new_asset_type.id)
    new_asset_2 = insert_new_asset(SECOND_NAME, new_asset_type.id)

    new_user = insert_new_user(FIRST_NAME)
    new_portfolio = insert_new_portfolio(FIRST_NAME, new_user.id)

    insert_new_portfolio_element(10.0, new_portfolio.id, new_asset_1.id)
    insert_new_portfolio_element(20.0, new_portfolio.id, new_asset_2.id)

    fetched_portfolio_elements = get_portfolio_all_elements(new_portfolio.id)

    assert fetched_portfolio_elements is not None
    assert len(fetched_portfolio_elements) == 2
    assert any(portfolio.order_fee == 10.0 for portfolio in fetched_portfolio_elements)
    assert any(portfolio.order_fee == 20.0 for portfolio in fetched_portfolio_elements)
    assert (portfolio.order_fee == 20.0 for portfolio in fetched_portfolio_elements)


def test_portfolio_element_deletion(session: Session):
    NAME = 'TPED'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)
    new_portfolio_element = insert_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    delete_portfolio_element(new_portfolio.id, new_portfolio_element.id)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                          asset_id=new_asset.id).first()
    assert fetched_portfolio_element is None


def test_get_portfolio_by_user_id(session: Session):
    FIRST_NAME = 'TGP1'
    SECOND_NAME = 'TGP2'
    new_user = insert_new_user(FIRST_NAME)
    portfolio1 = insert_new_portfolio(FIRST_NAME, new_user.id)
    portfolio2 = insert_new_portfolio(SECOND_NAME, new_user.id)

    fetched_portfolio_user_id = get_portfolios_by_user_id(new_user.id)
    assert fetched_portfolio_user_id is not None
    assert len(fetched_portfolio_user_id) == 2
    assert any(portfolio.name == FIRST_NAME for portfolio in fetched_portfolio_user_id)
    assert any(portfolio.name == SECOND_NAME for portfolio in fetched_portfolio_user_id)


def test_get_portfolio_by_id(session: Session):
    NAME = 'TGPBI'
    new_user = insert_new_user(NAME)
    portfolio = insert_new_portfolio(NAME, new_user.id)

    fetched_portfolio_by_id = get_portfolio_by_id(portfolio.id)
    assert fetched_portfolio_by_id is not None
    assert fetched_portfolio_by_id.name == NAME


def test_get_portfolio_by_name(session: Session):
    NAME = 'TGPBN'
    new_user = insert_new_user(NAME)
    portfolio = insert_new_portfolio(NAME, new_user.id)

    fetched_portfolio_by_name = get_portfolio_by_name(new_user.id, portfolio.name)
    assert fetched_portfolio_by_name is not None
    assert fetched_portfolio_by_name.name == NAME


def test_update_portfolio_name(session: Session):
    NAME = 'TUPN'
    NEW_NAME = 'new name'
    new_user = insert_new_user(NAME)
    portfolio = insert_new_portfolio(NAME, new_user.id)

    updated_portfolio = update_portfolio_name(portfolio.id, NEW_NAME)
    assert updated_portfolio is not None
    assert updated_portfolio.name == NEW_NAME


def test_portfolio_deletion(session: Session):
    NAME = 'TPD'
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)

    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion(session: Session):
    NAME = 'TCOPD'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)
    new_portfolio_element = insert_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

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
    NAME = 'TAI'
    new_asset_type = insert_new_asset_type(NAME)

    new_asset = add_new_asset(NAME, NAME, NAME, NAME, new_asset_type.id)

    fetched_asset = session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_get_asset_by_name(session: Session):
    NAME = 'TGABN'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)

    fetched_asset = get_asset_by_name(new_asset.name)

    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_asset_deletion(session: Session):
    NAME = 'TAD'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)

    delete_asset(new_asset.id)

    with pytest.raises(Exception):
        get_asset_by_name(NAME)


def test_asset_type_insertion(session: Session):
    NAME = 'TATI'
    new_asset_type = add_new_asset_type(NAME, NAME)

    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name

    with pytest.raises(Exception):
        add_new_asset_type(NAME, NAME)


def test_get_asset_type_by_name(session: Session):
    new_asset_type = insert_new_asset_type('TGATBN')

    fetched_asset_type = get_asset_type_by_name(new_asset_type.name)

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name


def test_asset_type_deletion(session: Session):
    NAME = 'TATD'
    new_asset_type = insert_new_asset_type(NAME)

    delete_asset_type(new_asset_type.id)
    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is None
