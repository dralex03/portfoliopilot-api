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
    resource = yf.Ticker(ticker)
    resource_info = resource.info

    return resource_info
