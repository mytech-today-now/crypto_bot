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
