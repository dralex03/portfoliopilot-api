from sqlalchemy.exc import NoResultFound
from src.database.connection import session
from src.database.models import Portfolio


def insert_portfolio(name, user_id):
    try:
        new_portfolio = Portfolio(
            name=name,
            user_id=user_id,
        )
        #  Create the new Portfolio

        session.add(new_portfolio)
        #  Add the new Portfolio to the session

        session.commit()
        #  Commit the Transaction

        print("Portfolio added successfully!")

    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to add portfolio: {e}")


def delete_portfolio_by_id(portfolio_id):
    try:
        portfolio_to_delete = session.query(Portfolio).filter_by(id=portfolio_id).one()
        #  Find the Portfolio to delete via ID

        session.delete(portfolio_to_delete)
        #  Delete the Portfolio

        session.commit()
        #  Commit the Transaction

        print(f"Portfolio with id {portfolio_id} deleted successfully!")
    except NoResultFound:
        print(f"No portfolio found with id {portfolio_id}")
    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to delete portfolio: {e}")


delete_portfolio_by_id(1)
