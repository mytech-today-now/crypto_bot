# html_logger_10.13.py

import os
import datetime


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
