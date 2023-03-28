# api_keys_10.13.py

import os

def get_exchange_api_key(exchange_name):
    """
    Returns the API key for the specified exchange from the environment variables.

    Parameters:
    exchange_name (str): The name of the exchange.

    Returns:
    str: The API key for the specified exchange.
    """
    api_key = os.environ.get(f"{exchange_name.upper()}_API_KEY")
    if api_key is None:
        raise ValueError(f"No API key found for {exchange_name}.")
    return api_key

def get_exchange_secret_key(exchange_name):
    """
    Returns the secret key for the specified exchange from the environment variables.

    Parameters:
    exchange_name (str): The name of the exchange.

    Returns:
    str: The secret key for the specified exchange.
    """
    secret_key = os.environ.get(f"{exchange_name.upper()}_SECRET_KEY")
    if secret_key is None:
        raise ValueError(f"No secret key found for {exchange_name}.")
    return secret_key