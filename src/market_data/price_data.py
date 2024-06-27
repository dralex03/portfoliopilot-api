import json

import yfinance as yf

valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


# TODO: not used yet
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

    if period not in valid_periods or interval not in valid_intervals:
        raise Exception("Invalid period or interval")

    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(period=period, interval=interval)

    # Reset index to make the DataFrame easier to convert to JSON
    df.reset_index(inplace=True)

    json_price_data = json.loads(df.to_json(orient='records', date_format='iso'))
    return json_price_data
