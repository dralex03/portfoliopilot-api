from sqlalchemy.exc import NoResultFound
from src.database.connection import session
from src.database.models import Portfolio, PortfolioElement, User


def add_portfolio(name, user_id):
    """
    Creates a portfolio based on the transferred name and ID of the user
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

        print('Portfolio added successfully!')
        return True

    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f'Failed to add portfolio: {e}')
        return False


def delete_portfolio_by_id(portfolio_id):
    """
    Deletes a portfolio based on the passed id
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

        print(f'Portfolio with id {portfolio_id} deleted successfully!')
        return True

    except NoResultFound:
        print(f'No portfolio found with id {portfolio_id}')
        return True

    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f'Failed to delete portfolio: {e}')
        return False


def insert_portfolio_element(portfolio_id, asset_id, count, buy_price, order_fee):
    """
    Adds the transferred portfolio element to the transferred portfolio
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
    existing_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                 asset_id=asset_id).first()
    #  Check if the added Asset already exists in the portfolio

    if existing_element:
        existing_element_total_buy_price = existing_element.buy_price * existing_element.count
        new_element_total_buy_price = buy_price * count
        combined_element_count = count + existing_element.count
        existing_element.buy_price = ((existing_element_total_buy_price +
                                       new_element_total_buy_price) / combined_element_count)
        #  Calculate the new buy price and overwrite the existing element with it

        existing_element.order_fee += order_fee
        #  Increase the order fee by the new order fee paid

        existing_element.count += count
        #  Increase the asset count by how much new assets have been added

        session.commit()
        #  Commit the Transaction

        print(f'Successfully increased the count of the asset {asset_id} in portfolio {portfolio_id}.')
        return True

    else:
        try:
            portfolio_element = PortfolioElement(count=count, buy_price=buy_price, order_fee=order_fee,
                                                 portfolio_id=portfolio_id, asset_id=asset_id)
            #  Create the new PortfolioElement

            session.add(portfolio_element)
            #  Add the Element to the Session

            session.commit()
            #  Commit the Transaction

            print(f'Successfully inserted asset.')
            return True
        except Exception as e:
            session.rollback()
            #  Roll back the Transaction due to an error

            print(f'Failed to insert asset: {e}')
            return False


def remove_portfolio_element(portfolio_id, asset_id, count=-1):
    """
    Deletes or reduces the count of a portfolio item from the transferred portfolio
        Parameters:
            int portfolio_id
            int asset_id
            int count (optional)
        Returns:
            Boolean: True if the portfolio element was successfully deleted or reduced, else False
        Raises:
            Value Error: If portfolio_id or asset_id are not int
    """

    try:
        target_portfolio_element = session.query(PortfolioElement).filter_by(portfolio_id=portfolio_id,
                                                                             asset_id=asset_id).one()
        #  Find the PortfolioElement to delete via the ID of the Portfolio and Asset

        if 0 < count < target_portfolio_element.count:
            target_portfolio_element.count = target_portfolio_element.count - count
            #  Reduce the count of the portfolio element

        else:
            session.delete(target_portfolio_element)
            #  Delete the PortfolioElement

        session.commit()
        #  Commit the Transaction

        print(f'PortfolioElement with portfolio_id {portfolio_id} and with asset_id {asset_id} deleted successfully!')
        return True

    except NoResultFound:
        print(f'No PortfolioElement found with portfolio_id {portfolio_id} and asset_id {asset_id}')
        return True
    except Exception as e:
        session.rollback()
        #  Roll back the Transaction due to an error

        print(f'Failed to delete PortfolioElement: {e}')
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
        print(f'Failed to insert User: {e}')
        session.rollback()
        return None
