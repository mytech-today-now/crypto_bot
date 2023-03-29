import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from typing import List, Tuple
from datetime import datetime

from db_manager import DBManager


class ARIMAModel:
    """
    ARIMA model class for predicting cryptocurrency prices
    """

    def __init__(self, crypto_symbol: str, db_manager: DBManager):
        """
        Initialize the ARIMA model instance

        :param crypto_symbol: Symbol of the cryptocurrency
        :type crypto_symbol: str
        :param db_manager: Instance of the database manager class
        :type db_manager: DBManager
        """
        self.crypto_symbol = crypto_symbol
        self.db_manager = db_manager

    def train(self, end_date: datetime, start_date: datetime, p: int, d: int, q: int):
        """
        Train the ARIMA model using historical data

        :param end_date: End date for the historical data
        :type end_date: datetime
        :param start_date: Start date for the historical data
        :type start_date: datetime
        :param p: Order of the autoregressive part of the model
        :type p: int
        :param d: Degree of differencing
        :type d: int
        :param q: Order of the moving average part of the model
        :type q: int
        """
        df = self.db_manager.get_historical_prices(self.crypto_symbol, end_date, start_date)
        df = df.reindex(index=df.index[::-1])

        model = ARIMA(df, order=(p, d, q))
        self.model_fit = model.fit()

    def predict(self, end_date: datetime, num_periods: int) -> List[Tuple[datetime, float]]:
        """
        Predict future cryptocurrency prices using the trained ARIMA model

        :param end_date: End date for the predicted prices
        :type end_date: datetime
        :param num_periods: Number of periods to predict
        :type num_periods: int
        :return: List of tuples containing predicted dates and prices
        :rtype: List[Tuple[datetime, float]]
        """
        start_date = end_date - pd.DateOffset(days=num_periods)

        df = self.db_manager.get_historical_prices(self.crypto_symbol, end_date, start_date)
        df = df.reindex(index=df.index[::-1])

        fcst, _, _ = self.model_fit.forecast(steps=num_periods)

        fcst_dates = pd.date_range(end=end_date, periods=num_periods + 1, freq='D')[1:]
        fcst_dates = [datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') for date in fcst_dates]

        return list(zip(fcst_dates, fcst))
