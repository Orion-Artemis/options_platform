import numpy as np
import pandas as pd
import yfinance as yf

def get_options(ticker):
    """
    Get the options for a given ticker symbol.
    params:
        ticker: str - the ticker symbol to get options for
    returns:
        dict - a dictionary containing the ticker symbol and options data
    """

    ticker_obj = yf.Ticker(ticker)
    expiration_date = ticker_obj.options[:5]
    if not expiration_date:
        print(f"Error getting options for {ticker}")
        return None

    options = []
    for expiration in expiration_date:
        try:
            options_chain = ticker_obj.option_chain(expiration)
            calls = options_chain.calls.head(10).fillna('None').to_dict('records')  # Replace NaN with None
            puts = options_chain.puts.head(10).fillna('None').to_dict('records')    # Replace NaN with None
        except Exception as e:
            print(f"Error getting option chain for {ticker} at expiration {expiration}: {e}")
            continue
        
        options.append({
            "expiration_date": expiration,
            "calls": calls,
            "puts": puts
        })
    return {
        "ticker": ticker,
        "options": options
    }
