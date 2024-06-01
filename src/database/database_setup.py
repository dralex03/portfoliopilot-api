from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.database_models import Base
from src.config import DATABASE_URL


try:
    #  Creates a base class for all ORM models
    engine = create_engine(DATABASE_URL)
    #  Creates Database Tables if they do not already exist
    Base.metadata.create_all(engine)
    #  Creates a session that gives query function context on which database they need to perform operations
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f'Error creating connection to database: {e}')
