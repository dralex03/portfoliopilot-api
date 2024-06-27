import yfinance as yf


def get_general_info(ticker: str):
    """
    Returns all information about a ticker from yahoo finance.
        Parameters:
            str ticker;
        Returns:
            dict: Information about the ticker symbol.
    """
    ticker_obj = yf.Ticker(ticker)

    if ticker_obj.info.get('symbol') is None:
        return None
    else:
        ticker_info = ticker_obj.info

        isin = ticker_obj.isin
        if not isin == '-':
            ticker_info['isin'] = isin

        return ticker_obj.info