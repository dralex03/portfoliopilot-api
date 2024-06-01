from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.database_models import Base
from src.config import DATABASE_URL


try:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f'Error creating connection to database: {e}')
