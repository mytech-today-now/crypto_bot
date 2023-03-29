import os
import ccxt
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import ssl
import time
import threading
from datetime import datetime, timedelta
from typing import List

################################################################################
# api_keys_10.13.py

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

################################################################################
# config_10.13.py

# API keys
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.environ.get("BINANCE_SECRET_KEY")

COINBASE_API_KEY = os.environ.get("COINBASE_API_KEY")
COINBASE_SECRET_KEY = os.environ.get("COINBASE_SECRET_KEY")
COINBASE_PASSPHRASE = os.environ.get("COINBASE_PASSPHRASE")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_SECRET_KEY = os.environ.get("GEMINI_SECRET_KEY")

# Email settings
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")

# Trading settings
TRADE_SYMBOL = os.environ.get("TRADE_SYMBOL", "BTC/USDT")
TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT", 100.0))
TRADE_STRATEGY = os.environ.get("TRADE_STRATEGY", "MACD")

# This file defines all the configuration variables required by the application, including API keys for different exchanges, email settings, and trading settings. The API keys are retrieved securely from environment variables, increasing the security of the program. The file also includes comments to explain the purpose of each configuration variable.

################################################################################
# exchange_api_10.13.py

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

################################################################################
# html_logger_10.13.py

class HtmlLogger:
    """
    Class for creating an HTML log file to record all of the bot's transactions
    """
    def __init__(self, file_name):
        """
        Initializes HtmlLogger class with the specified file name
        """
        self.file_name = file_name
        self.html_file = None

    def __enter__(self):
        """
        Method for setting up the HTML file for logging
        """
        self.html_file = open(self.file_name, "w")
        self.html_file.write("<html>\n")
        self.html_file.write("<body>\n")
        self.html_file.write("<h1>Bot Transaction Log</h1>\n")
        self.html_file.write("<table>\n")
        self.html_file.write("<tr><th>Date (UTC)</th><th>Local Time</th><th>Currency</th><th>Amount</th></tr>\n")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Method for closing the HTML file after logging is complete
        """
        self.html_file.write("</table>\n")
        self.html_file.write("</body>\n")
        self.html_file.write("</html>\n")
        self.html_file.close()

    def log_transaction(self, currency, amount):
        """
        Method for logging a transaction to the HTML file
        """
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        utc_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        price = 0  # TODO: get current price from exchange API
        total = price * amount
        self.html_file.write(f"<tr><td>{utc_time}</td><td>{local_time}</td><td>{currency}</td><td>{amount}</td></tr>\n")

################################################################################
# notification_10.13.py

class EmailNotifier:
    def __init__(self):
        self.from_email = config.EMAIL_FROM
        self.to_email = config.EMAIL_TO
        self.subject = config.EMAIL_SUBJECT
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.smtp_username = config.SMTP_USERNAME
        self.smtp_password = config.SMTP_PASSWORD
        self.ssl_context = ssl.create_default_context()

    def send_email(self, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = self.subject
            msg.attach(MIMEText(message, 'html'))
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.ssl_context)
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.from_email, self.to_email, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email: ", e)

################################################################################
# scheduler_10.13.py

# 2023-03-26
# Designer: mytechtoday@protonmail.com
# Coder: ChatGPT

# This file defines the Scheduler class, which handles the scheduling of recurring buy or sell orders based on the trading pairs and intervals specified in the config_10.13 file. The schedule_orders function creates a new instance of the Scheduler class and starts a new thread for it to run in. The thread runs the run method of the Scheduler class, which continuously checks if an order needs to be placed based on the current time and the specified intervals. If an order needs to be placed, it calls the place_order method of the ExchangeAPI class to place the order.
# The Scheduler class has a stop method that can be called to stop the scheduler and its thread from running. This is useful when the program needs to be shut down cleanly.
# The is_interval_due method checks if an interval is due based on the current time and the specified interval. It returns True if an interval is due, and False otherwise.


class Scheduler:
    def __init__(self, api: ExchangeAPI, trading_pairs: List[str], intervals: List[int]):
        self.api = api
        self.trading_pairs = trading_pairs
        self.intervals = intervals
        self.stopped = False

    def run(self):
        while not self.stopped:
            now = datetime.utcnow()
            for pair in self.trading_pairs:
                for interval in self.intervals:
                    if self._is_interval_due(now, interval):
                        self.api.place_order(pair, interval)
            time.sleep(60)

    def stop(self):
        self.stopped = True

    def _is_interval_due(self, now: datetime, interval: int) -> bool:
        return now.minute % interval == 0


def schedule_orders(api: ExchangeAPI, trading_pairs: List[str], intervals: List[int]):
    scheduler = Scheduler(api, trading_pairs, intervals)
    thread = threading.Thread(target=scheduler.run)
    thread.start()
    return scheduler, thread

################################################################################
# trading_bot_10.13.py

# 2023-03-26
# Designer: mytechtoday@protonmail.com
# Coder: ChatGPT

# This file defines the Scheduler class, which handles the scheduling of recurring buy or sell orders based on the trading pairs and intervals specified in the config_10.13 file. The schedule_orders function creates a new instance of the Scheduler class and starts a new thread for it to run in. The thread runs the run method of the Scheduler class, which continuously checks if an order needs to be placed based on the current time and the specified intervals. If an order needs to be placed, it calls the place_order method of the ExchangeAPI class to place the order.
# The Scheduler class has a stop method that can be called to stop the scheduler and its thread from running. This is useful when the program needs to be shut down cleanly.
# The is_interval_due method checks if an interval is due based on the current time and the specified interval. It returns True if an interval is due, and False otherwise.

from exchange_api import ExchangeAPI
from scheduler import Scheduler
from html_logger import HtmlLogger
from notification import EmailNotifier
from config import config

class TradingBot:
    """
    The main class for the trading bot application. It brings together all the other classes and functions to create a
    complete trading bot. It allows the user to configure the trading strategy, set up recurring orders, and view the bot's
    transactions through an HTML dashboard.
    """

    def __init__(self):
        # Create instances of required classes
        self.exchange_api = ExchangeAPI()
        self.scheduler = Scheduler(self.exchange_api)
        self.html_logger = HtmlLogger()
        self.notification = EmailNotifier()

    def run(self):
        """
        The main function that runs the trading bot.
        """
        # Get the current balances
        balances = self.exchange_api.get_balances()

        # Execute the configured trading strategy
        self.execute_trading_strategy(balances)

        # Schedule recurring orders
        self.scheduler.schedule_recurring_orders()

        # Log the transaction details in HTML format
        self.html_logger.log_transaction(balances)

        # Send email notification to the user
        self.notification.send_notification(balances)

    def execute_trading_strategy(self, balances):
        """
        The function that executes the trading strategy.
        """
        # Implement your trading strategy here using the balances and exchange_api

if __name__ == '__main__':
    bot = TradingBot()
    bot.run()

