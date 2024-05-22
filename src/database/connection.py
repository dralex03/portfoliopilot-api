import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.config import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f"Error establishing Database connection (Is .env correctly configured?): {e}")
    sys.exit(1)


def create_database():
    try:
        Base.metadata.create_all(engine)
        print("Database and tables created!")
    except Exception as e:
        print(f"Database could not be created: {e}")
        sys.exit(1)
