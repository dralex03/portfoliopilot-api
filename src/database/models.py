import uuid

from sqlalchemy import Column, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

from src.database.uuid_type import UUID


Base = declarative_base()

class Model(Base):
    """
    Abstract class to implement a functionality that the objects can be
    represented as a dictionary and can be parsed to JSON.
    """

    __abstract__ = True

    # Store values that shall be revealed in the json representation
    _json_values = []

    def to_json(self):
        """
        Custom function to return the object as a dictionary without any
        complex objects so that the dict can be parsed as JSON.
            Parameters:
                -
            Returns:
                dict: The object in dictionary format.
        """
        relationships = self.__mapper__.relationships.keys()
        
        if len(self._json_values) == 0:
            self._json_values = self.__table__.columns.keys()
        
        json_data = {}

        for key in self._json_values:
            if key in relationships:
                is_list = self.__mapper__.relationships[key].uselist

                if is_list:
                    json_data[key] = []
                    for item in getattr(self, key):
                        json_data[key].append(item.to_json())
                else:
                    if self.__mapper__.relationships[key].query_class is not None or self.__mapper__.relationships[key].instrument_class is not None:
                        json_data[key] = getattr(self, key).to_json()
                    else:
                        json_data[key] = getattr(self, key)
            else:
                json_data[key] = getattr(self, key)

        return json_data


class User(Model):
    __tablename__ = 'users'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    portfolios = relationship('Portfolio', back_populates='owner')

    _json_values = ['id', 'email', 'portfolios']


class Portfolio(Model):
    __tablename__ = 'portfolios'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(), ForeignKey('users.id'))
    owner = relationship('User', back_populates='portfolios')
    elements = relationship('PortfolioElement', back_populates='portfolio', cascade='all, delete-orphan')
    __table_args__ = (UniqueConstraint('name', 'user_id', name='portfolio_name_id_uc'),)

    _json_values = ['id', 'name', 'elements']


class PortfolioElement(Model):
    __tablename__ = 'portfolio_elements'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    count = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    order_fee = Column(Float, nullable=True)
    portfolio_id = Column(UUID(), ForeignKey('portfolios.id'))
    portfolio = relationship('Portfolio', back_populates='elements')
    asset_id = Column(UUID(), ForeignKey('assets.id'))
    asset = relationship('Asset', back_populates='portfolio_elements')

    _json_values = ['id', 'count', 'buy_price', 'order_fee', 'portfolio_id', 'asset']


class Asset(Model):
    __tablename__ = 'assets'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    ticker_symbol = Column(String, unique=True, nullable=False)
    isin = Column(String, unique=True, nullable=True)
    default_currency = Column(String, nullable=True)
    asset_type_id = Column(UUID(), ForeignKey('asset_types.id'))
    asset_type = relationship('AssetType', back_populates='assets')
    portfolio_elements = relationship('PortfolioElement', back_populates='asset')

    _json_values = ['id', 'name', 'ticker_symbol', 'isin', 'default_currency', 'asset_type']


class AssetType(Model):
    __tablename__ = 'asset_types'
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    quote_type = Column(String, unique=True, nullable=False)
    unit_type = Column(String, nullable=False)
    assets = relationship('Asset', back_populates='asset_type')

    _json_values = ['id', 'name', 'quote_type', 'unit_type']
