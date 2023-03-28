# scheduler_10.13.py

# 2023-03-26
# Designer: mytechtoday@protonmail.com
# Coder: ChatGPT

# This file defines the Scheduler class, which handles the scheduling of recurring buy or sell orders based on the trading pairs and intervals specified in the config_10.13 file. The schedule_orders function creates a new instance of the Scheduler class and starts a new thread for it to run in. The thread runs the run method of the Scheduler class, which continuously checks if an order needs to be placed based on the current time and the specified intervals. If an order needs to be placed, it calls the place_order method of the ExchangeAPI class to place the order.
# The Scheduler class has a stop method that can be called to stop the scheduler and its thread from running. This is useful when the program needs to be shut down cleanly.
# The is_interval_due method checks if an interval is due based on the current time and the specified interval. It returns True if an interval is due, and False otherwise.


import time
import threading

from datetime import datetime, timedelta
from typing import List

from config import TRADING_PAIRS, INTERVALS
from exchange_api import ExchangeAPI


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
