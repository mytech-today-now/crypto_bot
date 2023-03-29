import sqlite3
from datetime import datetime
from typing import List, Tuple

from binance_api import BinanceAPI
from coinbase_api import CoinbaseAPI
from gemini_api import GeminiAPI
from lstm_model import LSTMModel
from arima_model import ARIMAModel
from gpt3_model import GPT3Model
from email_notification import EmailNotification
from scheduler import Scheduler
from config import Config


class TradingBot:
    """
    The main class for the trading bot application.
    """

    def __init__(self, exchange: str, api_key: str, secret_key: str):
        """
        Initializes the TradingBot object with the specified exchange and API credentials.

        :param exchange: The name of the exchange to use (e.g. "binance", "coinbase", "gemini").
        :param api_key: The API key for the exchange account.
        :param secret_key: The secret key for the exchange account.
        """
        self.exchange = exchange
        self.api_key = api_key
        self.secret_key = secret_key

        # Create an instance of the appropriate API class based on the exchange name
        if exchange.lower() == "binance":
            self.api = BinanceAPI(api_key, secret_key)
        elif exchange.lower() == "coinbase":
            self.api = CoinbaseAPI(api_key, secret_key)
        elif exchange.lower() == "gemini":
            self.api = GeminiAPI(api_key, secret_key)
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        # Initialize the AI models
        self.lstm_model = LSTMModel()
        self.arima_model = ARIMAModel()
        self.gpt3_model = GPT3Model()

        # Initialize the email notification system
        self.email_notification = EmailNotification()

        # Initialize the scheduler
        self.scheduler = Scheduler()

        # Load the user configuration settings from the SQLite database
        self.config = Config()
        self.config.load_settings()

    def run(self):
        """
        Runs the trading bot application.
        """
        # TODO: Implement the main trading bot logic
        pass

    def configure_trading_strategy(self, strategy: str):
        """
        Configures the trading strategy to use.

        :param strategy: The name of the trading strategy to use (e.g. "lstm", "arima", "gpt3").
        """
        if strategy.lower() == "lstm":
            self.trading_strategy = self.lstm_model.predict
        elif strategy.lower() == "arima":
            self.trading_strategy = self.arima_model.predict
        elif strategy.lower() == "gpt3":
            self.trading_strategy = self.gpt3_model.predict
        else:
            raise ValueError(f"Unsupported trading strategy: {strategy}")

    def set_recurring_order(self, symbol: str, quantity: float, interval: str):
        """
        Sets up a recurring order for the specified symbol and quantity.

        :param symbol: The cryptocurrency symbol to trade (e.g. "BTC", "ETH", "XRP").
        :param quantity: The quantity of the cryptocurrency to trade.
        :param interval: The interval at which to place the order (e.g. "daily", "weekly", "monthly").
        """
        now = datetime.now()
        if interval.lower() == "daily":
            next_run_time = now.replace(hour=0, minute=0, second=
