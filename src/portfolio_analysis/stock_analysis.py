from collections import Counter

from src.database.queries import get_ticker_symbols_of_portfolio
from src.market_data.stock_data import get_stock_classification


def get_stock_portfolio_distribution(portfolio_id: int):
    """
    Calculates the country and sector distribution of a given portfolio. Also gives back the average P/E
        Parameters:
            int portfolio_id;
        Returns:
            Tuple: country_weights, sector_weights, average_pe if data is available
    """
    tickers = get_ticker_symbols_of_portfolio(portfolio_id)

    countries = []
    sectors = []
    trailing_pes = []
    for ticker in tickers:
        country, sector, trailing_pe = get_stock_classification(ticker)
        if country:
            countries.append(country)
        if sector:
            sectors.append(sector)
        if trailing_pe:
            trailing_pes.append(trailing_pe)

    sum_of_countries = len(countries)
    sum_of_sectors = len(sectors)
    avg_trailing_pe = sum(trailing_pes) / len(trailing_pes)

    country_counts = Counter(countries)
    sector_counts = Counter(sectors)
    #  e.g. {'Information Technology': 3, 'Financials': 1}

    country_weights = {country: round(
        (count / sum_of_countries) * 100, 2) for country, count in country_counts.items()}
    sector_weights = {sector: round(
        (count / sum_of_sectors) * 100, 2) for sector, count in sector_counts.items()}

    return {
        "country_weights": country_weights,
        "sector_weights": sector_weights,
        "avg_trailing_pe": avg_trailing_pe
    }
