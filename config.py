# config_10.13.py

import os

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
