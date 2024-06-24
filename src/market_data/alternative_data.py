import yfinance as yf


def get_alternative__info(ticker: str):
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

    resource_data = {
        "shortName": resource_info.get("shortName", ""),
        "quoteType": resource_info.get("quoteType", ""),
        "expireDate": resource_info.get("expireDate", ""),
        "maxAge": resource_info.get("maxAge", ""),  # indicates how old the data is
        "priceHint": resource_info.get("priceHint", ""),  # indicates precision of Data
        "previousClose": resource_info.get("previousClose", ""),
        "open": resource_info.get("open", ""),
        "dayLow": resource_info.get("dayLow", ""),
        "volume": resource_info.get("volume", ""),
        "averageVolume": resource_info.get("averageVolume", "")
    }

    return resource_data
