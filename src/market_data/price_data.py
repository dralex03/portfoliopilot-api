import yfinance as yf
import psycopg2


def get_price_data(ticker: str, period: str, interval: str):
    """
    Args:
        ticker:
        period:  (Valid is “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”)
        interval: (Valid is “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”)

    Returns:
        JSON PriceData object
    """
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(period=period, interval=interval)

    # Reset index to make the DataFrame easier to convert to JSON
    df.reset_index(inplace=True)

    json_data = df.to_json(orient='records', date_format='iso')
    return json_data

