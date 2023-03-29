import os

class Config:
    """This class contains all the configuration variables that are required by the application"""

    # Exchange API keys
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
    COINBASE_SECRET_KEY = os.getenv('COINBASE_SECRET_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_SECRET_KEY = os.getenv('GEMINI_SECRET_KEY')

    # Email notification settings
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
    EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')

    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL')
