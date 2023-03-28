# exchange_api_10.13.py

import ccxt
from api_keys import get_exchange_api_key, get_exchange_secret_key

class ExchangeAPI:
    """
    A class to interact with different cryptocurrency exchanges, including Binance, Coinbase, and Gemini.
    """
    def __init__(self, exchange_name):
        """
        Initializes the ExchangeAPI object.

        Args:
        exchange_name (str): The name of the exchange (e.g. 'binance', 'coinbase', 'gemini').
        """
        self.exchange_name = exchange_name
        self.exchange = self.get_exchange()

    def get_exchange(self):
        """
        Creates and returns an instance of the ccxt exchange object for the specified exchange.

        Returns:
        (ccxt.Exchange): An instance of the ccxt exchange object for the specified exchange.
        """
        # Load the API key and secret for the specified exchange
        api_key, api_secret = get_exchange_secret_key(self.exchange_name)

        # Create the ccxt exchange object
        exchange_class = getattr(ccxt, self.exchange_name)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })

        return exchange

    def get_balance(self, symbol):
        """
        Returns the balance for the specified cryptocurrency symbol.

        Args:
        symbol (str): The symbol of the cryptocurrency (e.g. 'BTC', 'ETH').

        Returns:
        (float): The balance of the cryptocurrency.
        """
        balance = self.exchange.fetch_balance()[symbol]['free']
        return balance

    def market_buy(self, symbol, amount):
        """
        Executes a market buy order for the specified cryptocurrency symbol and amount.

        Args:
        symbol (str): The symbol of the cryptocurrency to buy (e.g. 'BTC', 'ETH').
        amount (float): The amount of the cryptocurrency to buy.

        Returns:
        (str): The order ID for the buy order.
        """
        order = self.exchange.create_market_buy_order(symbol, amount)
        return order['id']

    def market_sell(self, symbol, amount):
        """
        Executes a market sell order for the specified cryptocurrency symbol and amount.

        Args:
        symbol (str): The symbol of the cryptocurrency to sell (e.g. 'BTC', 'ETH').
        amount (float): The amount of the cryptocurrency to sell.

        Returns:
        (str): The order ID for the sell order.
        """
        order = self.exchange.create_market_sell_order(symbol, amount)
        return order['id']

    def get_order(self, order_id, symbol):
        """
        Returns the status of the specified order.

        Args:
        order_id (str): The ID of the order.
        symbol (str): The symbol of the cryptocurrency (e.g. 'BTC', 'ETH').

        Returns:
        (dict): A dictionary with the order status.
        """
        order = self.exchange.fetch_order(order_id, symbol)
        return order
