from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import sqlalchemy

Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    portfolios = relationship('Portfolio', back_populates='owner')

class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='portfolios')
    elements = relationship('PortfolioElement', back_populates='portfolio')

class PortfolioElement(Base):
    __tablename__ = 'portfolio_elements'
    id = Column(Integer, primary_key=True)
    count = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    order_fee = Column(Float, nullable=True)
    buy_datetime = Column(DateTime, nullable=False)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    portfolio = relationship('Portfolio', back_populates='elements')
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relationship('Asset', back_populates='portfolio_elements')

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ticker_symbol = Column(String, unique=True, nullable=False)
    isin = Column(String, unique=True, nullable=True)
    default_currency = Column(String, nullable=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))
    asset_type = relationship('AssetType', back_populates='assets')
    portfolio_elements = relationship('PortfolioElement', back_populates='asset')

class AssetType(Base):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit_type = Column(String, nullable=False)
    assets = relationship('Asset', back_populates='asset_type')
