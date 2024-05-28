from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Portfolio, PortfolioElement, User
from src.database.queries import insert_new_user


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def init_test_db():
    session = Session()

    user1 = User(email='test1@example.com', password='<PASSWORD>')

    session.add(user1)
    session.commit()

    return session


test_session = init_test_db()

users = test_session.query(User).all()
for user in users:
    print(f'User {user.password} with email {user.email}')

