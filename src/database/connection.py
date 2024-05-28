from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.config import DATABASE_URL


try: 
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f'Error establishing Database connection: {e}')

def create_database():
    try:
        Base.metadata.create_all(engine) 
        print('Database tables created!')
    except Exception as e:
        print(f'Database tables could not be created: {e}')
