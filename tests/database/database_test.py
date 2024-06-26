import pytest

from src.database.queries import *
from src.database.setup import engine, Session
from src.database.models import *


@pytest.fixture(scope='function', autouse=True)
def setup_session():
    # Check for SQLite for test environment
    if not engine.url.get_backend_name() == 'sqlite':
        raise RuntimeError('Use SQLite Database to run tests')
    
    Base.metadata.create_all(engine)
    try:
        # Creates a session and gives it to the testing function
        with Session() as session:
            yield session
    finally:
        # Cleans up database after tests have run
        Base.metadata.drop_all(engine)


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


def test_user_insertion():
    USER_EMAIL = 'UR@example.com'
    PASSWORD = '<PASSWORD>'
    add_new_user(USER_EMAIL, PASSWORD)

    fetched_user = session.query(User).filter_by(email=USER_EMAIL).first()
    assert fetched_user is not None
    assert fetched_user.email == USER_EMAIL

    with pytest.raises(Exception):
        add_new_user(USER_EMAIL, PASSWORD)


def test_user_deletion():
    new_user = insert_new_user('UD')

    delete_user_by_id(new_user.id)

    fetched_user = session.query(User).filter_by(email=new_user.email).first()
    assert fetched_user is None


def test_get_user_by_email():
    new_user = insert_new_user('TGUBE')

    user = get_user_by_email(new_user.email)
    assert user is not None
    assert user.email == new_user.email


def test_portfolio_insertion():
    new_user = insert_new_user('TPI')

    PORTFOLIO_NAME = 'Welt portfolio'
    add_portfolio(PORTFOLIO_NAME, new_user.id)

    fetched_portfolio = session.query(Portfolio).filter_by(name=PORTFOLIO_NAME, user_id=new_user.id).first()
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == PORTFOLIO_NAME
    assert fetched_portfolio.user_id == new_user.id


def test_portfolio_element_insertion():
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


def test_portfolio_element_update():
    NAME = 'TPER'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)
    new_portfolio_element = insert_new_portfolio_element(10.0, new_portfolio.id, new_asset.id)

    update_portfolio_element(new_portfolio.id, new_asset.id, 5.0)

    fetched_portfolio_element = session.query(PortfolioElement).filter_by(id=new_portfolio_element.id).first()
    assert fetched_portfolio_element is not None
    assert fetched_portfolio_element.portfolio_id == new_portfolio.id
    assert fetched_portfolio_element.asset_id == new_asset.id
    assert fetched_portfolio_element.count == 5.0


def test_get_portfolio_all_elements():
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


def test_portfolio_element_deletion():
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


def test_get_portfolio():
    FIRST_NAME = 'TGP1'
    SECOND_NAME = 'TGP2'
    new_user = insert_new_user(FIRST_NAME)
    insert_new_portfolio(FIRST_NAME, new_user.id)
    insert_new_portfolio(SECOND_NAME, new_user.id)

    fetched_portfolio = get_portfolio_by_user_id(new_user.id)
    assert fetched_portfolio is not None
    assert len(fetched_portfolio) == 2
    assert any(portfolio.name == FIRST_NAME for portfolio in fetched_portfolio)
    assert any(portfolio.name == SECOND_NAME for portfolio in fetched_portfolio)


def test_portfolio_deletion():
    NAME = 'TPD'
    new_user = insert_new_user(NAME)
    new_portfolio = insert_new_portfolio(NAME, new_user.id)

    delete_portfolio_by_id(new_portfolio.id)

    fetched_portfolio = session.query(Portfolio).filter_by(id=new_portfolio.id).first()
    assert fetched_portfolio is None


def test_consequences_of_portfolio_deletion():
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

    fetched_asset_type = session.query(Asset).filter_by(id=new_asset_type.id).first()
    assert fetched_asset_type is not None


def test_asset_insertion():
    NAME = 'TAI'
    new_asset_type = insert_new_asset_type(NAME)

    new_asset = add_new_asset(NAME, NAME, NAME, NAME, new_asset_type.id)

    fetched_asset = session.query(Asset).filter_by(id=new_asset.id).first()
    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_get_asset_by_name():
    NAME = 'TGABN'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)

    fetched_asset = get_asset_by_name(new_asset.name)

    assert fetched_asset is not None
    assert fetched_asset.name == new_asset.name


def test_asset_deletion():
    NAME = 'TAD'
    new_asset_type = insert_new_asset_type(NAME)
    new_asset = insert_new_asset(NAME, new_asset_type.id)

    delete_asset(new_asset.id)

    with pytest.raises(Exception):
        get_asset_by_name(new_asset.name)


def test_asset_type_insertion():
    NAME = 'TATI'
    new_asset_type = add_new_asset_type(NAME, NAME)

    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name

    with pytest.raises(Exception):
        add_new_asset_type(NAME, NAME)


def test_get_asset_type_by_name():
    new_asset_type = insert_new_asset_type('TGATBN')

    fetched_asset_type = get_asset_type_by_name(new_asset_type.name)

    assert fetched_asset_type is not None
    assert fetched_asset_type.name == new_asset_type.name


def test_asset_type_deletion():
    NAME = 'TATD'
    new_asset_type = insert_new_asset_type(NAME)

    delete_asset_type(new_asset_type.id)
    fetched_asset_type = session.query(AssetType).filter_by(id=new_asset_type.id).first()

    assert fetched_asset_type is None
