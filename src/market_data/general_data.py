from multiprocessing import Process, Queue

import yfinance as yf


def get_isin(ticker: str, queue: Queue):
    """
    Helper function that fetches ISIN from the ticker object
    and puts it in a queue to give back to caller.
        Parameters:
            str ticker;
            Queue queue;
        Returns:
            -
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        isin = ticker_obj.isin
        queue.put(isin)
    except Exception as e:
        queue.put('-')


def get_general_info(ticker: str):
    """
    Returns all information about a ticker from yahoo finance.
        Parameters:
            str ticker;
        Returns:
            dict: Information about the ticker symbol.
    """
    ticker_obj = yf.Ticker(ticker)

    if ticker_obj.info.get('symbol') is None:
        return None

    ticker_info = ticker_obj.info

    # Use multiprocessing for custom 5sec timeout as default timeout
    # from yfinance is 30sec.
    queue = Queue()
    process = Process(target=get_isin, args=(ticker, queue))
    process.start()
    process.join(timeout=5)

    if process.is_alive():
        # terminate the process if it's still running
        process.terminate()
        process.join()
    else:
        # get the result from the queue and put it into return dict
        isin = queue.get()
        if isin != '-':
            ticker_info['isin'] = isin

    return ticker_info
