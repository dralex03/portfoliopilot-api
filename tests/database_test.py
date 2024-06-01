from src.database.database import database
from src.database.database_models import Portfolio, User, Asset, AssetType, PortfolioElement
from src.database.database_queries import insert_new_user, add_portfolio, insert_portfolio_element, \
    get_user_by_email, delete_portfolio_by_id, reduce_portfolio_element, delete_portfolio_element, \
    call_database_function


def add_new_user(name: str):
    new_user = User(email=name, password=name)
    database.session.add(new_user)
    database.session.commit()
    return new_user


def add_new_portfolio(name: str, user_id: int):
    new_portfolio = Portfolio(name=name, user_id=user_id)
    database.session.add(new_portfolio)
    database.session.commit()
    return new_portfolio


def add_new_portfolio_element(value: float, portfolio_id: int, asset_id: int):
    new_portfolio_element = PortfolioElement(portfolio_id=portfolio_id, asset_id=asset_id, count=value,
                                             buy_price=value, order_fee=value)
    database.session.add(new_portfolio_element)
    database.session.commit()
    return new_portfolio_element


def add_new_asset(name: str, asset_type_id: int):
    new_asset = Asset(name=name, ticker_symbol=name, isin=name, default_currency=name,
                      asset_type_id=asset_type_id)
    database.session.add(new_asset)
    database.session.commit()
    return new_asset


def add_new_asset_type(name: str):
    new_asset_type = AssetType(name=name, unit_type=name)
    database.session.add(new_asset_type)
    database.session.commit()
    return new_asset_type


def test_user_insertion():
    USER_EMAIL = 'UR@example.com'
    call_database_function(insert_new_user, USER_EMAIL, 'password')

    fetched_user = database.session.query(User).filter_by(email=USER_EMAIL).first()
    assert fetched_user is not None
    assert fetched_user.email == USER_EMAIL


def test_get_user_by_email():
    new_user = add_new_user('TGUBE')

    user = call_database_function(get_user_by_email, new_user.email)
    assert user is not None
    assert user.email == new_user.email


def test_portfolio_insertion():
    new_user = add_new_user('TPI')

    PORTFOLIO_NAME = 'Welt portfolio'
    call_database_function(add_portfolio, PORTFOLIO_NAME, new_user.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(name=PORTFOLIO_NAME, user_id=new_user.id).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == PORTFOLIO_NAME
    assert fetched_portfolio.user_id == new_user.id


def test_portfolio_element_insertion():
    new_asset_type = add_new_asset_type('TPEI')
    new_asset = add_new_asset('TPEI', new_asset_type.id)
    database.session.add(new_asset)
    new_user = add_new_user('TPEI')
    new_portfolio = add_new_portfolio('TPEI', new_user.id)

    call_database_function(insert_portfolio_element, new_portfolio.id, new_asset.id, 10.0, 10.0, 10.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                                   asset_id=new_asset.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.order_fee == 10.0
    assert fetched_portfolio_element.buy_price == 10.0
    assert fetched_portfolio_element.order_fee == 10.0


def test_portfolio_element_removal():
    new_asset_type = add_new_asset_type('TPER')
    new_asset = add_new_asset('TPER', new_asset_type.id)
    new_user = add_new_user('TPER')
    new_portfolio = add_new_portfolio('TPER', new_user.id)
    new_portfolio_element = add_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    call_database_function(reduce_portfolio_element, new_portfolio.id, new_asset.id, 5.0)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == 5.0


def test_portfolio_element_deletion():
    new_asset_type = add_new_asset_type('TPED')
    new_asset = add_new_asset('TPED', new_asset_type.id)
    new_user = add_new_user('TPED')
    new_portfolio = add_new_portfolio('TPED', new_user.id)
    new_portfolio_element = add_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    call_database_function(delete_portfolio_element, new_portfolio.id, new_asset.id)

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(portfolio_id=new_portfolio.id,
                                                                                   asset_id=new_asset.id).first()
    assert fetched_portfolio_element is None


def test_portfolio_deletion():
    new_user = add_new_user('TPD')
    new_portfolio = add_new_portfolio('TPD', new_user.id)

    call_database_function(delete_portfolio_by_id, new_portfolio.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion():
    new_asset_type = add_new_asset_type('TCOPD')
    new_asset = add_new_asset('TCOPD', new_asset_type.id)
    new_user = add_new_user('TCOPD')
    new_portfolio = add_new_portfolio('TCOPD', new_user.id)
    new_portfolio_element = add_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    call_database_function(delete_portfolio_by_id, new_portfolio.id)

    fetched_portfolio = database.session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None

    fetched_portfolio_element = database.session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is None

    fetched_asset = database.session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None

    fetched_asset_type = database.session.query(Asset).filter_by(id=new_asset_type.id).first()
    assert fetched_asset_type is not None
