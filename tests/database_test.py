from src.database.connection import database
from src.database.models import Portfolio, User, Asset, AssetType, PortfolioElement
from src.database.queries import insert_new_user, add_portfolio, insert_portfolio_element, \
    get_user_by_email, delete_portfolio_by_id, reduce_portfolio_element, delete_portfolio_element


def test_user_insertion():
    USER_EMAIL = 'UR@example.com'
    insert_new_user(USER_EMAIL, 'password')

    fetched_user = database.session.query(User).filter_by(email=USER_EMAIL).first()
    assert fetched_user is not None
    assert fetched_user.email == USER_EMAIL


def test_get_user_by_email():
    USER_EMAIL = 'GUBM@example.com'
    new_user = User(email=USER_EMAIL, password='1234')
    database.session.add(new_user)
    database.session.commit()

    user = get_user_by_email(USER_EMAIL)
    assert user is not None
    assert user.email == USER_EMAIL


def test_portfolio_insertion():
    USER_EMAIL = 'PE@example.com'
    new_user = User(email=USER_EMAIL, password='1234')
    database.session.add(new_user)
    database.session.commit()

    PORTFOLIO_NAME = 'Welt portfolio'
    add_portfolio(PORTFOLIO_NAME, new_user.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(name=PORTFOLIO_NAME, user_id=new_user.id).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == PORTFOLIO_NAME
    assert fetched_portfolio.user_id == new_user.id


def test_portfolio_element_insertion():
    new_asset_type = AssetType(name="PEI", unit_type="PEI")
    database.session.add(new_asset_type)
    database.session.commit()
    new_asset = Asset(name="PEI", ticker_symbol='PEI', isin='PEI', default_currency='PEI',
                      asset_type_id=new_asset_type.id)
    database.session.add(new_asset)
    new_user = User(email='PEI@example.com', password='PEI')
    database.session.add(new_user)
    database.session.commit()
    new_portfolio = Portfolio(name='PEI portfolio', user_id=new_user.id)
    database.session.add(new_portfolio)
    database.session.commit()

    insert_portfolio_element(new_portfolio.id, new_asset.id, 10.0, 10.0,10.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                                   asset_id=new_asset.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.order_fee == 10.0
    assert fetched_portfolio_element.buy_price == 10.0
    assert fetched_portfolio_element.order_fee == 10.0


def test_portfolio_element_removal():
    new_asset_type = AssetType(name="PER", unit_type="PER")
    database.session.add(new_asset_type)
    database.session.commit()
    new_asset = Asset(name="PER", ticker_symbol='PER', isin='PER', default_currency='PER',
                      asset_type_id=new_asset_type.id)
    database.session.add(new_asset)
    new_user = User(email='PER@example.com', password='PER')
    database.session.add(new_user)
    database.session.commit()
    new_portfolio = Portfolio(name='PER portfolio', user_id=new_user.id)
    database.session.add(new_portfolio)
    database.session.commit()
    new_portfolio_element = PortfolioElement(portfolio_id=new_portfolio.id, asset_id=new_asset.id, count=10.0,
                                             buy_price=10.0, order_fee=10.0)
    database.session.add(new_portfolio_element)
    database.session.commit()

    reduce_portfolio_element(new_portfolio.id, new_asset.id, 5.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == 5.0


def test_portfolio_element_deletion():
    new_asset_type = AssetType(name="PED", unit_type="PED")
    database.session.add(new_asset_type)
    database.session.commit()
    new_asset = Asset(name="PED AG", ticker_symbol='PED', isin='PED', default_currency='PED',
                      asset_type_id=new_asset_type.id)
    database.session.add(new_asset)
    new_user = User(email='PED@example.com', password='PED')
    database.session.add(new_user)
    database.session.commit()
    new_portfolio = Portfolio(name='PED Portfolio', user_id=new_user.id)
    database.session.add(new_portfolio)
    database.session.commit()
    new_portfolio_element = PortfolioElement(portfolio_id=new_portfolio.id, asset_id=new_asset.id, count=10.0,
                                             buy_price=10.0, order_fee=10.0)
    database.session.add(new_portfolio_element)
    database.session.commit()

    delete_portfolio_element(new_portfolio.id, new_asset.id)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                                   asset_id=new_asset.id).first()
    assert fetched_portfolio_element is None


def test_portfolio_deletion():
    new_user = User(email='PD@example.com', password='PD')
    database.session.add(new_user)
    database.session.commit()
    new_portfolio = Portfolio(name='PD Portfolio', user_id=new_user.id)
    database.session.add(new_portfolio)
    database.session.commit()

    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion():
    new_asset_type = AssetType(name="COPD", unit_type="COPD")
    database.session.add(new_asset_type)
    database.session.commit()
    new_asset = Asset(name="COPD AG", ticker_symbol='COPD', isin='COPD', default_currency='COPD',
                      asset_type_id=new_asset_type.id)
    database.session.add(new_asset)
    new_user = User(email='COPD@example.com', password='COPD')
    database.session.add(new_user)
    database.session.commit()
    new_portfolio = Portfolio(name='COPD Portfolio', user_id=new_user.id)
    database.session.add(new_portfolio)
    database.session.commit()
    new_portfolio_element = PortfolioElement(portfolio_id=new_portfolio.id, asset_id=new_asset.id, count=10.0,
                                             buy_price=10.0, order_fee=10.0)
    database.session.add(new_portfolio_element)
    database.session.commit()

    insert_portfolio_element(new_portfolio.id, new_asset.id, 10.0, 10.0, 10.00)
    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is None

    fetched_asset = database.session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None

    fetched_asset_type = database.session.query(Asset).filter_by(id=new_asset_type.id).first()
    assert fetched_asset_type is not None
