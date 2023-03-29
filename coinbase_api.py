import os
import requests

class CoinbaseAPI:
    """
    A class for interacting with the Coinbase cryptocurrency exchange API.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.api_key = os.getenv(f"{exchange}_API_KEY")
        self.api_secret = os.getenv(f"{exchange}_API_SECRET")

    def get_balance(self, currency):
        """
        Get the balance for a specific currency.
        """
        try:
            url = f"https://api.coinbase.com/v2/accounts?currency={currency}"
            response = requests.get(url, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "CB-ACCESS-SIGN": self.api_secret,
                "CB-ACCESS-TIMESTAMP": str(int(time.time())),
                "CB-ACCESS-KEY": self.api_key,
            })
            response.raise_for_status()
            data = response.json()
            return float(data["data"][0]["balance"]["amount"])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error: {e}")

    def place_order(self, order_type, currency_pair, amount, price=None):
        """
        Place an order to buy or sell a specific currency pair.
        """
        try:
            if order_type == "buy":
                url = "https://api.coinbase.com/v2/accounts/{}/buys".format(self.get_account_id(currency_pair))
                data = {
                    "amount": str(amount),
                    "currency": currency_pair.split("-")[0],
                    "payment_method": self.get_payment_method(),
                }
                if price is not None:
                    data["price"] = str(price)
            else:
                url = "https://api.coinbase.com/v2/accounts/{}/sells".format(self.get_account_id(currency_pair))
                data = {
                    "amount": str(amount),
                    "currency": currency_pair.split("-")[0],
                    "payment_method": self.get_payment_method(),
                }
                if price is not None:
                    data["price"] = str(price)
            response = requests.post(url, json=data, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "CB-ACCESS-SIGN": self.api_secret,
                "CB-ACCESS-TIMESTAMP": str(int(time.time())),
                "CB-ACCESS-KEY": self.api_key,
            })
            response.raise_for_status()
            data = response.json()
            return data["id"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error: {e}")

    def get_account_id(self, currency_pair):
        """
        Get the account ID for a specific currency pair.
        """
        try:
            response = requests.get("https://api.coinbase.com/v2/accounts", headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "CB-ACCESS-SIGN": self.api_secret,
                "CB-ACCESS-TIMESTAMP": str(int(time.time())),
                "CB-ACCESS-KEY": self.api_key,
            })
            response.raise_for_status()
            data = response.json()
            for account in data["data"]:
                if account["currency"] == currency_pair.split("-")[0]:
                    return account["id"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error: {e}")

    def get_payment_method(self):
        """
        Get the payment method for the Coinbase account.
        """
        try:
            response = requests.get("https://api.coinbase.com/v2/payment-methods", headers={
               
