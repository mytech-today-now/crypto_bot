from datetime import datetime
from typing import List, Tuple
import os


class HTMLLogger:
    """
    A class for creating an HTML log file to record all of the bot's transactions.
    """

    def __init__(self, log_directory: str = "logs"):
        """
        Constructor for HTMLLogger class.
        :param log_directory: The directory where log files will be saved.
        """
        self.log_directory = log_directory

        # Create the logs directory if it does not exist.
        if not os.path.exists(log_directory):
            os.mkdir(log_directory)

    def log_transaction(self, timestamp: int, exchange: str, pair: str, action: str, quantity: float, price: float):
        """
        Method for logging a transaction to an HTML file.
        :param timestamp: The Unix timestamp of the transaction.
        :param exchange: The name of the exchange where the transaction occurred.
        :param pair: The currency pair involved in the transaction.
        :param action: The type of transaction (buy or sell).
        :param quantity: The quantity of currency involved in the transaction.
        :param price: The price per unit of currency involved in the transaction.
        """
        # Create the log filename based on the date.
        date_string = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        log_filename = f"{self.log_directory}/{date_string}.html"

        # Create the log file if it does not exist.
        if not os.path.exists(log_filename):
            with open(log_filename, "w") as f:
                f.write(self._generate_html_header(date_string))

        # Generate the HTML log entry for the transaction.
        log_entry = self._generate_log_entry(timestamp, exchange, pair, action, quantity, price)

        # Write the log entry to the log file.
        with open(log_filename, "a") as f:
            f.write(log_entry)

    def _generate_html_header(self, date_string: str) -> str:
        """
        Method for generating the HTML header for the log file.
        :param date_string: The date string to be included in the title of the HTML file.
        :return: The HTML header string.
        """
        header = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{date_string} Log</title>\n</head>\n<body>\n"
        return header

    def _generate_log_entry(self, timestamp: int, exchange: str, pair: str, action: str, quantity: float, price: float) -> str:
        """
        Method for generating the HTML log entry for a transaction.
        :param timestamp: The Unix timestamp of the transaction.
        :param exchange: The name of the exchange where the transaction occurred.
        :param pair: The currency pair involved in the transaction.
        :param action: The type of transaction (buy or sell).
        :param quantity: The quantity of currency involved in the transaction.
        :param price: The price per unit of currency involved in the transaction.
        :return: The HTML log entry string.
        """
        log_entry = f"<p>{datetime.fromtimestamp(timestamp)} - {exchange} - {pair} - {action} - {quantity} - {price}</p>\n"
        return log_entry
