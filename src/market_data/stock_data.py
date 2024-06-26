import yfinance as yf


def get_stock_info(ticker: str):
    """
    Returns specific stock information from yahoo finance

    Args:
        str ticker

    Returns:
        JSON
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    # Formatting and adding insider buy information
    ticker_obj_insider_purchases = ticker_obj.insider_purchases.head(3)
    insider_data = ticker_obj_insider_purchases.to_dict(orient='records')
    info['insider_transactions'] = insider_data

    return info


def get_stock_classification(ticker: str):
    """
    Returns the country, sector and pe of a given stock ticker or None if this information is not available

    Args:
        str ticker

    Returns:
        JSON country, sector and trailingPE if Data is available
    """

    stock = yf.Ticker(ticker)
    if stock:
        return stock.info.get('country'), stock.info.get('sector'), stock.info.get('trailingPE')
    return None
