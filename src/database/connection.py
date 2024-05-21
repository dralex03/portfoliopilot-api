import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

try: 
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f"Error establishing Database connection: {e}")

def create_database():
    try:
        Base.metadata.create_all(engine) 
        print("Database and tables created!")
    except Exception as e:
        print(f"Database could not be created: {e}")

if __name__ == '__main__':
    create_database()