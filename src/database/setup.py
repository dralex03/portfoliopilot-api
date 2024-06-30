from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_URL
from src.constants.asset_types import ASSET_TYPES
from src.database.models import AssetType, Base

#  Creates a base class for all ORM models
engine = create_engine(DATABASE_URL)


#  Creates a session that gives query function context on which database they need to perform operations
Session = sessionmaker(bind=engine)
session = Session()


def create_db_schema():
    if not engine.url.get_backend_name() == 'postgresql':
        raise RuntimeError('Use PostgreSQL database to run production/dev!')
    try:
        #  Creates Database Tables if they do not already exist
        Base.metadata.create_all(engine)
        initialize_default_data()
    except Exception as e:
        print(f'Error creating database schema: {e}')


def initialize_default_data():

    # Use an extra session for adding default data
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for asset_type in ASSET_TYPES:
            name = asset_type.get('name')
            quote_type = asset_type.get('quoteType')
            unit_type = asset_type.get('unitType')

            existing_asset_type = session.query(
                AssetType).filter_by(name=name).first()

            # Add asset type if not existent yet
            if existing_asset_type is None:
                new_asset_type = AssetType(
                    name=name, quote_type=quote_type, unit_type=unit_type)
                session.add(new_asset_type)

        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
