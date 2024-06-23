import yfinance as yf


def get_stock_info(ticker: str):
    """
    Returns specific stock information from yahoo finance

    Args:
        ticker Stock ticker symbol

    Returns:
        JSON
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    ticker_obj_insider_purchases = ticker_obj.insider_purchases

    stock_data = {
        "ticker": ticker,
        "name": info.get("shortName", ""),
        "sector": info.get("sector", ""),
        "country": info.get("country", ""),
        "marketCap": info.get("marketCap", ""),
        "businessSummary": info.get("longBusinessSummary", ""),
        "fullTimeEmployees": info.get("fullTimeEmployees", ""),
        "dividendRate": info.get("dividendRate", ""),
        "fiveYearAvgDividendYield": info.get("fiveYearAvgDividendYield", ""),

        "sharesOutstanding": info.get("sharesOutstanding", ""),
        "sharesShort": info.get("sharesShort", ""),
        "heldPercentInsiders": info.get("heldPercentInsiders", ""),
        "heldPercentInstitutions": info.get("heldPercentInstitutions", ""),
        "insider_percentage_development_last_6_months": ticker_obj_insider_purchases.loc[ticker_obj_insider_purchases
                                                                ['Insider Purchases Last 6m'] ==
                                                                '% Net Shares Purchased (Sold)', 'Shares'].values[0],
        "trailingPE": info.get("trailingPE", ""),
        "forwardPE": info.get("forwardPE", ""),
        "trailingEps": info.get("trailingEps", ""),
        "forwardEps": info.get("forwardEps", ""),
        "bookValue": info.get("bookValue", ""),
        "totalRevenue": info.get("totalRevenue", ""),
        "revenuePerShare": info.get("revenuePerShare", ""),
        "profitMargins": info.get("profitMargins", ""),
        "totalCash": info.get("totalCash", ""),
        "totalCashPerShare": info.get("totalCashPerShare", ""),
        "totalDebt": info.get("totalDebt", ""),
        "debtToEquity": info.get("debtToEquity", ""),

        "earningsQuarterlyGrowth": info.get("earningsQuarterlyGrowth", ""),
        "freeCashflow": info.get("freeCashflow", ""),

        "recommendationKey": info.get("recommendationKey", ""),
        "targetHighPrice": info.get("targetHighPrice", ""),
        "targetMeanPrice": info.get("targetMeanPrice", ""),
        "targetLowPrice": info.get("targetLowPrice", ""),
        "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions", ""),

    }

    return stock_data


def get_stock_classification(ticker: str):
    """
    Returns the country and sector of a given stock ticker or None if this information is not available

    Args:
        ticker Stock ticker symbol

    Returns:
        Tuple Country, String or None, None if this information is not available
    """

    stock = yf.Ticker(ticker)
    if stock:
        return stock.info.get('country'), stock.info.get('sector')
    return None
