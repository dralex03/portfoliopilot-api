import yfinance as yf


def get_alternative_info(ticker: str):
    """
    Returns information about futures (especially including alternative investments like gold, silver etc.)
    and bonds
    Args:
        str ticker

    Returns:
        Json object
    """
    bond = yf.Ticker(ticker)
    bond_info = bond.info
    return bond_info

