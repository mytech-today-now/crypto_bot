import requests
import json

class BinanceAPI:
    """
    This class contains methods for interacting with the Binance API.
    """
    def __init__(self, api_key, secret_key):
        """
        Initializes the Binance API object with the provided API and secret keys.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.binance.com"

    def _get(self, endpoint, params={}):
        """
        Sends a GET request to the Binance API endpoint and returns the response.
        """
        try:
            response = requests.get(self.base_url + endpoint, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return None

    def _post(self, endpoint, params={}):
        """
        Sends a POST request to the Binance API endpoint and returns the response.
        """
        try:
            response = requests.post(self.base_url + endpoint, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return None

    def _get_headers(self):
        """
        Returns the headers required for Binance API requests.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.api_key
        }
        return headers

    def get_account_info(self):
        """
        Retrieves the account information from the Binance API.
        """
        endpoint = "/api/v3/account"
        response = self._get(endpoint)
        if response is not None and "balances" in response:
            return response["balances"]
        return None

    def get_order_book(self, symbol, limit=100):
        """
        Retrieves the order book for the specified symbol from the Binance API.
        """
        endpoint = "/api/v3/depth"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        response = self._get(endpoint, params)
        if response is not None and "bids" in response and "asks" in response:
            return response
        return None

    def place_order(self, symbol, side, type, quantity, price=None):
        """
        Places an order on the Binance exchange.
        """
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        if price is not None:
            params["price"] = price
        signature = self._generate_signature(params)
        params["signature"] = signature
        response = self._post(endpoint, params)
        if response is not None and "orderId" in response:
            return response
        return None

    def _generate_signature(self, params):
        """
        Generates the HMAC SHA256 signature for the Binance API request.
        """
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return hmac.new(self.secret_key.encode('utf-8
