from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.config import DATABASE_URL

#  Creates a base class for all ORM models
engine = create_engine(DATABASE_URL)

#  Creates a session that gives query function context on which database they need to perform operations
Session = sessionmaker(bind=engine)
session = Session()


def setup_database():
    try:
        #  Creates Database Tables if they do not already exist
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f'Error creating connection to database: {e}')
