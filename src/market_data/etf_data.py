from yahooquery import Ticker


def get_etf_info(ticker: str):
    info = Ticker(ticker)

    etf_data = {
        "fund_holding_info": info.fund_holding_info,
        "idk": info.fund_profile
    }

    return etf_data


print(get_etf_info("EUNL.DE"))

