import yfinance as yf


# TODO: not used yet
def get_stock_info(ticker: str):
    """
    Returns specific stock information from yahoo finance.
        Parameters:
            str ticker;
        Returns:
            dict: Information about the stock.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    # Formatting and adding insider buy information
    ticker_obj_insider_purchases = ticker_obj.insider_purchases.head(3)
    insider_data = ticker_obj_insider_purchases.to_dict(orient='records')
    info['insider_transactions'] = insider_data

    return info


# TODO: not used yet
def get_stock_classification(ticker: str):
    """
    Returns the country, sector and pe of a given stock ticker or None if this information is not available.
        Parameters:
            str ticker;
        Returns:
            Tuple: country, sector and trailingPE if Data is available 
            else None
    """

    stock = yf.Ticker(ticker)
    if stock:
        return stock.info.get('country'), stock.info.get('sector'), stock.info.get('trailingPE')
    return None
