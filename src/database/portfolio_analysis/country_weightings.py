from collections import Counter
from src.database.models import Portfolio, PortfolioElement, User, Asset, AssetType
from src.database.setup import session
from src.market_data.stock_data import get_stock_classification


def get_stock_portfolio_distribution(portfolio_id: int):
    """
    Berechnet die Länderverteilung und Sektorverteilung eines Aktienportfolios
    Args:
        portfolio_id:

    Returns:
        Tuple country_weights, sector_weights or None, None if the information is not available
    """
    tickers = (
        session.query(Asset.ticker_symbol)
        .join(PortfolioElement, PortfolioElement.asset_id == Asset.id)
        .filter(PortfolioElement.portfolio_id == portfolio_id)
        .all()
    )

    countries = []
    sectors = []
    for ticker in tickers:
        country, sector = get_stock_classification(ticker)
        if country:
            countries.append(country)
        if sector:
            sectors.append(sector)

    sum_of_countries = len(countries)
    sum_of_sectors = len(sectors)

    country_counts = Counter(countries)
    sector_counts = Counter(sectors)
    #  e.g. {'Information Technology': 3, 'Financials': 1}

    country_weights = {country: round((count / sum_of_countries) * 100, 2) for country, count in country_counts.items()}
    sector_weights = {sector: round((count / sum_of_sectors) * 100, 2) for sector, count in sector_counts.items()}

    return country_weights, sector_weights


