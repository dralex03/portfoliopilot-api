import yfinance as yf

valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


def get_price_data(ticker: str, period: str, interval: str):
    """
    Fetches price data of a given ticker over a specified period and interval
    Args:
        str ticker
        str period
        str interval

    Returns:
        JSON PriceData object
    """

    if period not in valid_periods or interval not in valid_intervals:
        raise Exception("Invalid period or interval")

    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(period=period, interval=interval)

    # Reset index to make the DataFrame easier to convert to JSON
    df.reset_index(inplace=True)

    json_price_data = df.to_json(orient='records', date_format='iso')
    return json_price_data


def get_current_price(ticker_symbol: str):
    """
    Fetches the most recent price of a given ticker symbol.
    Args:
        str ticker_symbol

    Returns:
        JSON price_data
    """

    ticker = yf.Ticker(ticker_symbol)

    recent_data = ticker.history(period='1d')

    most_recent_price = recent_data['Close'].iloc[-1]

    price_info = {"price": most_recent_price}

    return price_info


