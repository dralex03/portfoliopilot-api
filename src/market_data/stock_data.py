import yfinance as yf


def get_stock_classification(ticker: str):
    """
    Returns the country, sector and pe of a given stock ticker or None if this information is not available
        Parameters:
            str ticker
        Returns:
            JSON country, sector and trailingPE if Data is available
    """
    stock = yf.Ticker(ticker)
    if stock:
        info = stock.info
        ticker_type = info.get('quoteType')

        if ticker_type == 'EQUITY':
            return info.get('country'), info.get('sector'), info.get('trailingPE')

    return None
