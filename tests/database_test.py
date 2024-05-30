from src.database.connection import database
from src.database.models import Portfolio, PortfolioElement, User
from src.database.queries import insert_new_user, add_portfolio

import sys

sys.path.append('../src')


def test_user_insertion():
    #  Test if the user insert_new_user function works and returns the right result
    user = insert_new_user('testuser@example.com', 'password')
    assert user is not None
    assert user.email == 'testuser@example.com'

    #  Test if User really is in database
    fetched_user = database.session.query(User).filter_by(email='testuser@example.com').first()
    print(f'Debug: Fetched user: {fetched_user}')
    assert fetched_user is not None


def test_portfolio_insertion():
    portfolio = add_portfolio('Welt portfolio', 1)
    assert portfolio is True

    #  Test if Portfolio really is in database
    fetched_portfolio = database.session.query(Portfolio).filter_by(name='Welt portfolio', user_id=1).first()
    print(f'Debug: Fetched user: {fetched_portfolio}')
    assert fetched_portfolio is not None
    assert fetched_portfolio.name == 'Welt portfolio'
    assert fetched_portfolio.user_id == 1
