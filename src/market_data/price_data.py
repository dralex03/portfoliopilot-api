import json

import yfinance as yf

VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
VALID_INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


def get_price_data(ticker: str, period: str, interval: str):
    """
    Returns the price data in JSON format for a specific period and interval.
        Parameters:
            str ticker;
            str period;
            str interval;
        Returns:
            dict: PriceData for requested ticker in JSON format.
    """

    if period not in VALID_PERIODS or interval not in VALID_INTERVALS:
        raise Exception("Invalid period or interval")

    ticker_obj = yf.Ticker(ticker)
    if ticker_obj.info.get('symbol') is None:
        return None
    else:
        df = ticker_obj.history(period=period, interval=interval, raise_errors=True)

        # Reset index to make the DataFrame easier to convert to JSON
        df.reset_index(inplace=True)

        json_price_data = json.loads(df.to_json(orient='records', date_format='iso'))
        return json_price_data


def get_current_price(ticker_symbol: str):
    """
    Fetches the most recent price of a given ticker symbol.
        Parameters:
            str ticker_symbol
        Returns:
            JSON price_data
    """

    ticker = yf.Ticker(ticker_symbol)

    if ticker.info.get('symbol') is None:
        return None

    recent_data = ticker.history(period='1d')

    most_recent_price = recent_data['Close'].iloc[-1]

    price_info = {"price": most_recent_price}

    return price_info
