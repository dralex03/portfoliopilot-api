import yfinance as yf


# TODO: not used yet
def get_alternative_info(ticker: str):
    """
    Returns information about futures (especially including alternative investments like gold, silver etc.)
    and bonds
        Parameters:
            str ticker;
        Returns:
            dict: Information about the future.
    """
    resource = yf.Ticker(ticker)
    resource_info = resource.info

    return resource_info
