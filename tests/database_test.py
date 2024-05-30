import logging
from src.database.connection import database
from src.database.models import Portfolio, User, Asset, AssetType, PortfolioElement
from src.database.queries import insert_new_user, add_portfolio, insert_portfolio_element, \
    get_user_by_email, delete_portfolio_by_id, reduce_portfolio_element

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USER_EMAIL = 'testuser@example.com'


def setup_database():
    """Manually adds an asset type plus asset as these functions do not yet exist"""
    new_asset_type = AssetType(id=1, name="Aktien", unit_type="idk")
    database.session.add(new_asset_type)

    new_asset = Asset(id=1, name="Test AG", ticker_symbol='TAG', isin='ISIN123', default_currency='DOLLAR',
                      asset_type_id=1)
    database.session.add(new_asset)
    database.session.commit()


setup_database()


def test_user_insertion():
    insert_new_user(USER_EMAIL, 'password')

    fetched_user = database.session.query(User).filter_by(email=USER_EMAIL).first()
    assert fetched_user is not None
    assert fetched_user.email == USER_EMAIL


def test_get_user_by_email():
    user = get_user_by_email(USER_EMAIL)
    assert user is not None
    assert user.email == USER_EMAIL


def test_portfolio_insertion():
    PORTFOLIO_NAME = 'Welt portfolio'
    add_portfolio(PORTFOLIO_NAME, 1)

    fetched_portfolio = database.session.query(Portfolio).filter_by(name=PORTFOLIO_NAME, user_id=1).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == PORTFOLIO_NAME
    assert fetched_portfolio.user_id == 1


def test_portfolio_element_insertion():
    insert_portfolio_element(1, 1, 10.0, 10.0,
                             10.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == 1
    assert fetched_portfolio_element.asset_id == 1
    assert fetched_portfolio_element.order_fee == 10.0
    assert fetched_portfolio_element.buy_price == 10.0
    assert fetched_portfolio_element.order_fee == 10.0


def test_portfolio_element_removal():
    reduce_portfolio_element(1, 1, 5.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.count == 5.0
    assert fetched_portfolio_element.portfolio_id == 1
    assert fetched_portfolio_element.asset_id == 1


def test_portfolio_element_deletion():
    portfolio_element_deletion = delete_portfolio_by_id(1)
    assert portfolio_element_deletion is True

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    assert fetched_portfolio_element is None


def test_portfolio_deletion():
    portfolio_deletion = delete_portfolio_by_id(1)
    assert portfolio_deletion is True

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=1).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion():
    portfolio = add_portfolio("Test Portfolio", 1)
    id_to_remove = portfolio.id

    insert_portfolio_element(id_to_remove, 1, 10.0, 10.0, 10.00)
    delete_portfolio_by_id(id_to_remove)

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=id_to_remove).first()
    assert fetched_portfolio is None

    fetched_asset = database.session.query(Asset).filter_by(id=1).first()
    assert fetched_asset is not None

    fetched_asset_type = database.session.query(Asset).filter_by(id=1).first()
    assert fetched_asset_type is not None
