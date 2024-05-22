from sqlalchemy.exc import NoResultFound
from src.database.connection import session
from src.database.models import Portfolio, PortfolioElement


def add_portfolio(name, user_id):
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


def insert_portfolio_element(portfolio_id, asset_id, count, buy_price, order_fee):
    existing_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                           asset_id=asset_id).first()
    #  Check if the added Asset already exists in the portfolio

    if existing_portfolio_element:
        existing_portfolio_element_paid_money = existing_portfolio_element.buy_price * existing_portfolio_element.count
        new_portfolio_element_paid_money = buy_price * count
        portfolio_element_combined_count = count + existing_portfolio_element.count
        existing_portfolio_element.buy_price = ((existing_portfolio_element_paid_money +
                                                 new_portfolio_element_paid_money) / portfolio_element_combined_count)
        #  Calculate the new buy price and adjust it

        existing_portfolio_element.order_fee += order_fee
        #  Increase the order fee by the new order fee paid

        existing_portfolio_element.count += count
        #  Increase the asset count by how much new assets have been added

    else:
        try:
            portfolio_element = PortfolioElement(count=count, buy_price=buy_price, order_fee=order_fee,
                                                 portfolio_id=portfolio_id, asset_id=asset_id)
            #  Create the new PortfolioElement

            session.add(portfolio_element)
            #  Add the Element to the Session

            session.commit()
            #  Commit the Transaction

            print(f"Successfully inserted asset.")
        except Exception as e:
            session.rollback()
            #  Roll back the Transaction due to an error

            print(f"Failed to insert asset: {e}")


def delete_portfolio_element(portfolio_id, asset_id):
    try:
        portfolio_element_to_delete = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                                asset_id=asset_id).one()
        #  Find the PortfolioElement to delete via the ID of the Portfolio and Asset

        session.delete(portfolio_element_to_delete)
        #  Delete the PortfolioElement

        session.commit()
        #  Commit the Transaction

        print(f"PortfolioElement with portfolio_id {portfolio_id} and with asset_id {asset_id} deleted successfully!")
    except NoResultFound:
        print(f"No PortfolioElement found with portfolio_id {portfolio_id} and asset_id {asset_id}")
    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to delete PortfolioElement: {e}")


