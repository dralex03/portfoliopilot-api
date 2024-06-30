import yahooquery

from src.constants.asset_types import QUOTE_TYPE_LIST


def search_assets(query: str, country: str|None = None):
    """
    Uses yahooquery to find assets for the passed query filtered
    by quote types that are set in the database.
        Parameters:
            str query;
            str|None country;
        Returns:
            dict: The search results and a the number of results.
    """

    # Use yahooquery for the search
    result = yahooquery.search(query, quotes_count=20, country=country, news_count=0)

    if result.get('count') > 0:
        quotes = result.get('quotes')
        quotes_result = [
            q for q in quotes if q.get('quoteType') in QUOTE_TYPE_LIST
        ]

        return {
            'count': len(quotes_result),
            'assets': quotes_result
        }
    else:
        return {
            'count': 0,
            'assets': []
        }

