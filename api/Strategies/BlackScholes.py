import pandas as pd

# Black-Scholes formula for call options
from math import log, sqrt, exp
from scipy.stats import norm


def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price for a call option.
    
    :param S: Current stock price
    :param K: Strike price
    :param T: Time to maturity (in years)
    :param r: Risk-free interest rate
    :param sigma: Volatility of the stock (implied volatility)
    :return: Call option price
    """
    d1 = (log(S / K) + (r + (sigma**2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    return call_price

def calculate_greeks(S, K, T, r, sigma):
    """
    Calculate the Greeks for a call option.
    
    :param S: Current stock price
    :param K: Strike price
    :param T: Time to maturity (in years)
    :param r: Risk-free interest rate
    :param sigma: Volatility of the stock (implied volatility)
    :return: Dictionary containing the calculated Greeks (Delta, Gamma, Theta, Vega, Rho)
    """
    
    d1 = (log(S / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * sqrt(T))
    theta = -(S * norm.pdf(d1) * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * norm.cdf(d2)
    vega = S * norm.pdf(d1) * sqrt(T)
    rho = K * T * exp(-r * T) * norm.cdf(d2)
    return {"Delta": delta, "Gamma": gamma, "Theta": theta, "Vega": vega, "Rho": rho}



def evaluate_call_option(option_data, risk_free_rate=0.05):
    """
    Evaluate if a call option is favorable based on Black-Scholes price, premium, and breakeven.

    :param option_data: Dictionary containing option and data details
    :param risk_free_rate: Risk-free interest rate (default: 0.05)
    :return: A dictionary with the evaluation results
    """
    # Extract the expiration date and option details
    expiration_date = pd.Timestamp(option_data['data'][0], tz='UTC')  # Expiration date
    option_details = option_data['data'][1]  # Nested dictionary containing option details
    lastTradeDate = pd.Timestamp(option_details['lastTradeDate'], tz='UTC') # Last trade date

    # Extract relevant fields from option_details
    S = option_details['lastPrice']  # Current stock price
    K = option_details['strike']  # Strike price
    T = (expiration_date - lastTradeDate).days / 365  # Time to maturity in years
    sigma = option_details['impliedVolatility']  # Implied volatility
    bid = option_details['bid']
    ask = option_details['ask']

    # Calculate Black-Scholes price
    black_scholes_price = black_scholes_call(S, K, T, risk_free_rate, sigma)

    # Calculate premium (midpoint of bid and ask)
    premium_paid = (bid + ask) / 2

    # Calculate breakeven price
    breakeven_price = K + premium_paid

    # Calculate intrinsic value
    intrinsic_value = max(S - K, 0)

    # Calculate time value
    time_value = premium_paid - intrinsic_value

    # Determine favorability
    is_favorable = black_scholes_price >= premium_paid and breakeven_price <= S * 1.1  # 10% margin for breakeven

    # Calculate the Greeks (Delta, Gamma, Theta, Vega, Rho)
    greeks = calculate_greeks(S, K, T, risk_free_rate, sigma)

    # Create evaluation result
    evaluation_result = {
        'Black-Scholes Price': black_scholes_price,
        'Premium Paid': premium_paid,
        'Breakeven Price': breakeven_price,
        'Intrinsic Value': intrinsic_value,
        'Time Value': time_value,
        'Is Favorable': is_favorable,
        'Greeks': greeks
    }

    return evaluation_result