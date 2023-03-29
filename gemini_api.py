import requests
import hmac
import hashlib
import time
import json

class GeminiAPI:
    """
    This class contains the functions for interacting with the Gemini cryptocurrency exchange API. It handles the API requests 
    and responses and provides a unified interface for the application to communicate with Gemini.
    """
    
    BASE_URL = "https://api.gemini.com"
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        
    def get_signature(self, request_body, nonce):
        """
        This function generates the signature for the API request.
        """
        signature_payload = f"{nonce}{json.dumps(request_body)}"
        signature = hmac.new(self.api_secret.encode(), signature_payload.encode(), hashlib.sha384).hexdigest()
        return signature
        
    def get_headers(self, request_body):
        """
        This function generates the headers for the API request.
        """
        nonce = int(time.time() * 1000)
        signature = self.get_signature(request_body, nonce)
        headers = {
            "Content-Type": "text/plain",
            "Content-Length": "0",
            "X-GEMINI-APIKEY": self.api_key,
            "X-GEMINI-PAYLOAD": json.dumps(request_body),
            "X-GEMINI-SIGNATURE": signature,
            "Cache-Control": "no-cache"
        }
        return headers
    
    def get_ticker(self, symbol):
        """
        This function returns the ticker information for the specified symbol.
        """
        endpoint = f"{self.BASE_URL}/v1/pubticker/{symbol}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Error getting ticker information from Gemini.")
        
    def get_order_book(self, symbol):
        """
        This function returns the order book for the specified symbol.
        """
        endpoint = f"{self.BASE_URL}/v1/book/{symbol}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Error getting order book from Gemini.")
    
    def get_balance(self):
        """
        This function returns the balance for the account associated with the API key.
        """
        endpoint = f"{self.BASE_URL}/v1/balances"
        request_body = {"request": "/v1/balances", "nonce": int(time.time() * 1000)}
        headers = self.get_headers(request_body)
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Error getting balance information from Gemini.")
        
    def new_order(self, symbol, amount, price, side, order_type):
        """
        This function places a new order with the specified parameters.
        """
        endpoint = f"{self.BASE_URL}/v1/order/new"
        request_body = {
            "request": "/v1/order/new",
            "nonce": int(time.time() * 1000),
            "symbol": symbol,
            "amount": str(amount),
            "price": str(price),
            "side": side,
            "type": order_type
        }
        headers = self.get_headers(request_body)
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Error placing order with Gemini.")
        
    def cancel_order(self, order_id):
        """
        This function cancels the order with the specified order ID.
        """
        endpoint = f"{self.BASE_URL}/v1/order
