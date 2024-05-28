from sqlalchemy.exc import NoResultFound
from src.database.connection import session
from src.database.models import Portfolio, PortfolioElement, User


def add_portfolio(name, user_id):
    """
        Erstellt ein Portfolio anhand des übergebenen Namens und der Id des Nutzers
            Parameters:
                str name
                int user_id
            Returns:
                Boolean: True if the portfolio was successfully created, else False
            Raises:
                Value Error: If name is not str or user_id not int
    """
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
        return True

    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to add portfolio: {e}")
        return False


def delete_portfolio_by_id(portfolio_id):
    """
        Löscht ein Portfolio anhand der übergebenen id
            Parameters:
                int portfolio_id
            Returns:
                Boolean: True if the portfolio was successfully deleted, else False
            Raises:
                Value Error: If portfolio_id is not int
    """
    try:
        portfolio_to_delete = session.query(Portfolio).filter_by(id=portfolio_id).one()
        #  Find the Portfolio to delete via ID

        session.delete(portfolio_to_delete)
        #  Delete the Portfolio

        session.commit()
        #  Commit the Transaction

        print(f"Portfolio with id {portfolio_id} deleted successfully!")
        return True

    except NoResultFound:
        print(f"No portfolio found with id {portfolio_id}")
        return False

    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to delete portfolio: {e}")
        return False


def insert_portfolio_element(portfolio_id, asset_id, count, buy_price, order_fee):
    """
        Fügt dem übergebenem Portfolio das übergebene Portfolio Element hinzu
            Parameters:
                int portfolio_id
                int asset_id
                float count
                float buy_price
                float order_fee
            Returns:
                Boolean: True if the portfolio element was successfully added, else False
            Raises:
                Value Error: If portfolio_id, asset_id are not int and if count, buy_price or order_fee are not a Number
    """
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
    """
    Löscht ein Portfolio Element aus dem übergebenem Portfolio
        Parameters:
            int portfolio_id
            int asset_id
        Returns:
            Boolean: True if the portfolio element was successfully deleted, else False
        Raises:
            Value Error: If portfolio_id or asset_id are not int
    """
    
    try:
        portfolio_element_to_delete = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                                asset_id=asset_id).one()
        #  Find the PortfolioElement to delete via the ID of the Portfolio and Asset

        session.delete(portfolio_element_to_delete)
        #  Delete the PortfolioElement

        session.commit()
        #  Commit the Transaction

        print(f"PortfolioElement with portfolio_id {portfolio_id} and with asset_id {asset_id} deleted successfully!")
        return True

    except NoResultFound:
        print(f"No PortfolioElement found with portfolio_id {portfolio_id} and asset_id {asset_id}")
        return False
    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f"Failed to delete PortfolioElement: {e}")
        return False

def get_user_by_email(email):
    """
    Fetches a user by email from the database
        Parameters:
            email: str
        Returns:
            User: user object
    """

    return session.query(User).filter(User.email == email).first()

def insert_new_user(email, password):
    """
    Inserts new user into database and returns the created object
        Parameters:
            email: str
            password: str
        Returns:
            User: created user object
    """

    try:
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        print('Error inserting new user: ' + e)
        return None
