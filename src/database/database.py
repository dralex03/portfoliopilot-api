import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.database_models import Base
from src.config import DATABASE_URL


class Database:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)

        self.create_database()

        self.session = self.create_session()

    def create_session(self):
        try:
            Session = sessionmaker(bind=self.engine)
            return Session()
        except Exception as e:
            print(f'Error establishing Database connection (Is .env correctly configured?): {e}')
            sys.exit(1)

    def create_database(self):
        """Creates the database Tables if they do not exist already."""
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f'Database could not be created: {e}')
            sys.exit(1)

    def get_session(self):
        return self.session


database = Database(DATABASE_URL)
