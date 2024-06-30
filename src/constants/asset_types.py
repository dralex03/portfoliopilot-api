ASSET_TYPES = [
    {
        'name': 'Stocks',
        'quoteType': 'EQUITY',
        'unitType': 'Share'
    },
    {
        'name': 'ETFs',
        'quoteType': 'ETF',
        'unitType': 'Share'
    },
    {
        'name': 'Crypto Currencies',
        'quoteType': 'CRYPTOCURRENCY',
        'unitType': 'Coin'
    },
    {
        'name': 'Futures',
        'quoteType': 'FUTURE',
        'unitType': 'Contract'
    },
    {
        'name': 'Options',
        'quoteType': 'OPTION',
        'unitType': 'Option'
    }
]

QUOTE_TYPE_LIST = [
    t.get('quoteType') for t in ASSET_TYPES
]