from yfinance.exceptions import YFChartError
from src.market_data.price_data import get_current_price


@assets.route('/ticker/<ticker>/currentPrice', methods=['GET'])
def ticker_current_price(ticker: str):
    """
    Handles GET requests to /assets/ticker/<ticker>/currentPrice,
    used to get the current price data of a specific ticker.
        Parameters:
            str ticker;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    try:
        current_price = get_current_price(ticker)
    except Exception as e:  # pragma: no cover
        return generate_internal_error_response(
            ApiErrors.Assets.ticker_price_data_error, e
        )

    # Check if asset with this ticker exists
    if current_price is None:
        return generate_not_found_response(ApiErrors.Assets.ticker_not_found)

    return generate_success_response(current_price)
