from yahooquery import Ticker


def get_etf_info(ticker: str):
    """
    Returns specific basic etf information from yahoo finance.
        Parameters:
            str ticker;
        Returns:
            dict: Information about the ETF.
        """
    info = Ticker(ticker)

    etf_data = {
        'fund_holding_info': info.fund_holding_info,
        'fund_profile': info.fund_profile
    }

    return etf_data
