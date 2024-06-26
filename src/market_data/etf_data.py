from yahooquery import Ticker


def get_etf_info(ticker: str):
    """
        Returns specific basic etf information from yahoo finance

        Args:
            str ticker

        Returns:
            JSON etf_data
        """
    info = Ticker(ticker)

    etf_data = {
        'fund_holding_info': info.fund_holding_info,
        'fund_profile': info.fund_profile
    }

    return etf_data