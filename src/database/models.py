from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    portfolios = relationship('Portfolio', back_populates='owner')


class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='portfolios')
    elements = relationship('PortfolioElement', back_populates='portfolio', cascade='all, delete-orphan')
    __table_args__ = (UniqueConstraint('name', 'user_id', name='portfolio_name_id_uc'),)


class PortfolioElement(Base):
    __tablename__ = 'portfolio_elements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)
    order_fee = Column(Float, nullable=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    portfolio = relationship('Portfolio', back_populates='elements')
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relationship('Asset', back_populates='portfolio_elements')


class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ticker_symbol = Column(String, unique=True, nullable=False)
    isin = Column(String, unique=True, nullable=True)
    default_currency = Column(String, nullable=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))
    asset_type = relationship('AssetType', back_populates='assets')
    portfolio_elements = relationship('PortfolioElement', back_populates='asset')


class AssetType(Base):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    unit_type = Column(String, nullable=False)
    assets = relationship('Asset', back_populates='asset_type')
