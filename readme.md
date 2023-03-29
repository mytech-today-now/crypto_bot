# Trading Bot Application

---

**Name**: ChatBTC Cryptotrading Bot
**Designer**: kyle@mytech.today
**Coder**: ChatGPT-4
**Created**: 2023-03-27 - Version 10.3 - developed basic application with notification and logging.
**Updated**: 2023-03-28 - Version 15.2 - added SQLite DB to manage records and configurations.  Added AI trading models.

---

About Author:

I, ChatGPT-4, have coded all of Version 1 through Version 15.2 of the ChatBTC Cryptotrading Bot, while Kyle shaped the design and managed development. As of Tuesday, March 28, 2023 @ 18:00 PST, only 10 hours have been committed to the project within the span of two days.

You can follow the development of this application via chat in the chat.txt file.
---

**Version: 15.2**

---

## Overview

Version 15.2 of the Application is a trading bot that allows users to configure their trading strategy, set up recurring orders, and view the bot's transactions through an HTML dashboard. The application is built using Python, HTML, CSS, and JavaScript, and uses SQLite to manage the bot's transaction records, user settings, AI models, and logs.

Version 15.2 of the Application:

## Features

- Automated trading process
- Support for multiple exchanges
- Recurring order scheduling
- Configurable trading strategy
- HTML dashboard for viewing transactions
- Customizable user interface

## File Descriptions

- `config.py`: Config class: handles all the configuration variables that are required by the application, including API keys for different exchanges, email settings, and other application settings.
- `api_keys.py`: 
  - get_api_key(exchange_name: str, key_name: str) -> str: function for getting an API key from the environment variables.
  - set_api_key(exchange_name: str, key_name: str, key_value: str): function for setting an API key in the environment variables.
- `exchange_api.py`: Contains the classes and functions for interacting with different cryptocurrency exchanges. It handles the API requests and responses and provides a unified interface for the application to communicate with different exchanges.
- `html_logger.py`: Contains the class for creating an HTML log file to record all of the bot's transactions. It includes the date, time, currency involved, and amount of the transaction.
- `notification.py`: Contains the class for sending email notifications to the user. It includes the option to configure the email settings in the config file.
- `scheduler.py`: Contains the class for scheduling recurring buy or sell orders, such as daily or weekly. It allows the user to automate the trading process and make it more efficient.
- `trading_bot.py`: Contains the main class for the trading bot application. It brings together all the other classes and functions to create a complete trading bot. It allows the user to configure the trading strategy, set up recurring orders, and view the bot's transactions through an HTML dashboard.
- `dashboard.html`: Contains the HTML code for the trading bot dashboard. It includes a customizable user interface that allows users to change the color scheme, font size, and layout of the dashboard view.
- `dashboard.css`: Contains the CSS code for styling the trading bot dashboard. It allows users to customize the appearance of the dashboard to their liking.
- `dashboard.js`: Contains the JavaScript code for the trading bot dashboard. It includes the logic for updating the dashboard in real-time, displaying the bot's transactions, and allowing users to customize the UI.
- `binance_api.py`: BinanceAPI class: contains the methods and functions for interacting with the Binance cryptocurrency exchange API. It handles the API requests and responses and provides a unified interface for the application to communicate with Binance.
- `coinbase_api.py`: CoinbaseAPI class: contains the methods and functions for interacting with the Coinbase cryptocurrency exchange API. It handles the API requests and responses and provides a unified interface for the application to communicate with Coinbase.
- `gemini_api.py`: GeminiAPI class: contains the methods and functions for interacting with the Gemini cryptocurrency exchange API. It handles the API requests and responses and provides a unified interface for the application to communicate with Gemini.
- `email_notification.py`: EmailNotification class: contains the methods and functions for sending email notifications to the user. It includes the option to configure the email settings in the SQLite database table.
- `scheduler.py`: Scheduler class: contains the methods and functions for scheduling recurring buy or sell orders, such as daily or weekly. It allows the user to automate the trading process and make it more efficient. The user configuration settings are stored in the SQLite database table.
- `lstm_model.py`: LSTMModel class: contains the methods and functions for the LSTM AI model that can be used to predict cryptocurrency prices. It provides an interface for adding additional LSTM models. The user configuration settings are stored in the SQLite database table.
- `arima_model.py`: ARIMAModel class: contains the methods and functions for the ARIMA AI model that can be used to predict cryptocurrency prices. It provides an interface for adding additional ARIMA models. The user configuration settings are stored in the SQLite database table.
- `gpt3_model.py`: GPT3Model class: contains the methods and functions for the GPT-3 AI model that can be used to predict cryptocurrency prices. It provides an interface for adding additional GPT-3 models. The user configuration settings are stored in the SQLite database table.
- `trading_bot.py`: TradingBot class: contains the methods and functions for the trading bot application. It brings together all the other classes and functions to create a complete trading bot. It allows the user to configure the trading strategy, set up recurring orders, and view the bot's transactions through an HTML dashboard. The user configuration settings are stored in the SQLite database table.
- `dashboard.html`: This file contains the HTML code for the trading bot dashboard. It includes a customizable user interface that allows users to change the color scheme, font size, and layout of the dashboard view.
- `dashboard.css`: This file contains the CSS code for styling the trading bot dashboard. It allows users to customize the appearance of the dashboard to their liking.
- `dashboard.js`: This file contains the JavaScript code for the trading bot dashboard. It includes the logic for updating and displaying.
- `transactoions.db`: The SQLite database of table with user configuration settings, bot settings, and transaction log files.


## transactions.db:

The SQL code for creating the four database tables in the transactions.db file:

```
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    exchange TEXT,
    pair TEXT,
    action TEXT,
    quantity REAL,
    price REAL
);

CREATE TABLE config (
    id INTEGER PRIMARY KEY,
    name TEXT,
    value TEXT
);

CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    type TEXT,
    version TEXT,
    file_path TEXT
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    level TEXT,
    message TEXT
);
```