import os
import sqlite3

class ApiKeys:
    """
    Class for managing API keys securely.
    """
    def __init__(self, exchange):
        """
        Initializes the ApiKeys class with the specified exchange name.
        """
        self.exchange = exchange
        self.conn = sqlite3.connect('trading_bot.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def __del__(self):
        """
        Closes the database connection when the object is destroyed.
        """
        self.conn.close()

    def create_table(self):
        """
        Creates a new table for the exchange if it does not exist.
        """
        try:
            self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.exchange}_api_keys
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                api_key TEXT NOT NULL,
                                secret_key TEXT NOT NULL)''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table for {self.exchange}: {str(e)}")
            self.conn.rollback()

    def insert_keys(self, api_key, secret_key):
        """
        Inserts the API and secret keys into the table for the exchange.
        """
        try:
            self.cur.execute(f"INSERT INTO {self.exchange}_api_keys (api_key, secret_key) VALUES (?, ?)",
                              (api_key, secret_key))
            self.conn.commit()
            print(f"API keys added for {self.exchange}.")
        except Exception as e:
            print(f"Error inserting API keys for {self.exchange}: {str(e)}")
            self.conn.rollback()

    def update_keys(self, api_key, secret_key):
        """
        Updates the API and secret keys in the table for the exchange.
        """
        try:
            self.cur.execute(f"UPDATE {self.exchange}_api_keys SET api_key = ?, secret_key = ? WHERE id = 1",
                              (api_key, secret_key))
            self.conn.commit()
            print(f"API keys updated for {self.exchange}.")
        except Exception as e:
            print(f"Error updating API keys for {self.exchange}: {str(e)}")
            self.conn.rollback()

    def get_keys(self):
        """
        Retrieves the API and secret keys from the table for the exchange.
        """
        try:
            self.cur.execute(f"SELECT api_key, secret_key FROM {self.exchange}_api_keys WHERE id = 1")
            keys = self.cur.fetchone()
            return keys
        except Exception as e:
            print(f"Error getting API keys for {self.exchange}: {str(e)}")
            return None

    def remove_keys(self):
        """
        Deletes the API and secret keys from the table for the exchange.
        """
        try:
            self.cur.execute(f"DELETE FROM {self.exchange}_api_keys WHERE id = 1")
            self.conn.commit()
            print(f"API keys removed for {self.exchange}.")
        except Exception as e:
            print(f"Error removing API keys for {self.exchange}: {str(e)}")
            self.conn.rollback()

    def get_env_var(self, key):
        """
        Retrieves the API or secret key from the environment variables.
        """
        try:
            return os.environ[key]
        except Exception as e:
            print(f"Error retrieving {key} from environment variables: {str(e)}")
            return None
