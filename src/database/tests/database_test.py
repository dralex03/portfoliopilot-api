import logging
from src.database.connection import database
from src.database.models import Portfolio, User, Asset, AssetType, PortfolioElement
from src.database.queries import insert_new_user, add_portfolio, insert_portfolio_element, remove_portfolio_element, \
                                 get_user_by_email, delete_portfolio_by_id

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_email = 'testuser@example.com'


def setup_database():
    """Manually adds an asset type plus asset as these functions do not yet exist"""
    new_asset_type = AssetType(1, 'Aktien')
    database.session.add(new_asset_type)

    new_asset = Asset(1, 'Test A', 'TAG', 'ISIN1234', 'DOLLAR', 1)
    database.session.add(new_asset)
    database.session.commit()


setup_database()


def test_user_insertion():
    logger.info('Starting test_user_insertion')
    user = insert_new_user(user_email, 'password')
    assert user is not None
    assert user.email == user_email
    logger.debug(f'Inserted user: {user}')

    fetched_user = database.session.query(User).filter_by(email=user_email).first()
    logger.debug(f'Fetched user: {fetched_user}')
    assert fetched_user is not None


def test_get_user_by_email():
    logger.info('Starting to find test_user')
    user = get_user_by_email(user_email)
    assert user is not None
    assert user.email == user_email
    logger.debug(f'Found user: {user}')


def test_portfolio_insertion():
    logger.info('Starting test_portfolio_insertion')
    portfolio = add_portfolio('Welt portfolio', 1)
    assert portfolio is True
    logger.debug(f'Portfolio was inserted: {portfolio}')

    fetched_portfolio = database.session.query(Portfolio).filter_by(name='Welt portfolio', user_id=1).first()
    logger.debug(f'Fetched portfolio: {fetched_portfolio}')
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == 'Welt portfolio'
    assert fetched_portfolio.user_id == 1


def test_portfolio_element_insertion():
    logger.info('Starting test_portfolio_element_insertion')
    portfolio_element = insert_portfolio_element('Welt portfolio', 1, 10.0, 10.0,
                                                 10.0)
    assert portfolio_element is True

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    logger.debug(f'Fetched portfolio: {fetched_portfolio_element}')
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == 1
    assert fetched_portfolio_element.asset_id == 1


def test_portfolio_element_removal():
    logger.info('Starting test_portfolio_element removal')
    portfolio_element = remove_portfolio_element(1, 1, 5.00)
    assert portfolio_element is True

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    logger.debug(f'Fetched portfolio: {fetched_portfolio_element}')
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.count == 5.00
    assert fetched_portfolio_element.portfolio_id == 1
    assert fetched_portfolio_element.asset_id == 1


def test_portfolio_deletion():
    logger.info('Starting test_portfolio_deletion')
    portfolio = delete_portfolio_by_id(1)
    assert portfolio is True

    fetched_portfolio = database.session.query(Portfolio).filter_by(portfolio_id=1).first()
    logger.debug(f'Search Results for Portfolio after Deletion: {fetched_portfolio}')
    assert fetched_portfolio is None

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=1, asset_id=1).first()
    logger.debug(f'Search Results for Portfolio_Element after Deletion: {fetched_portfolio_element}')
    assert fetched_portfolio_element is None
