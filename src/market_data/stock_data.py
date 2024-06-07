import yfinance as yf
import json


def get_stock_info(ticker: str):
    """
    Args:
        ticker: Stock ticker symbol

    Returns:
        str: JSON with stock information including name, sector, and price data
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    # Create a dictionary to hold the stock data
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

        "trailingPE": info.get("trailingPE", ""),
        "forwardPE": info.get("forwardPE", ""),
        "trailingEps": info.get("trailingEps", ""),
        "forwardEps": info.get("forwardEps", ""),
        "bookValue": info.get("bookValue", ""),
        "totalRevenue": info.get("totalRevenue", ""),
        "profitMargins": info.get("profitMargins", ""),
        "revenuePerShare": info.get("revenuePerShare", ""),
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


print(get_stock_info("TSLA"))