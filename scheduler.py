import sqlite3
import time

class Scheduler:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.cursor = self.conn.cursor()

    def create_order(self, order_type, symbol, quantity, price):
        """
        Creates a new buy or sell order with the given parameters.
        """
        try:
            # validate input
            if order_type not in ['buy', 'sell']:
                raise ValueError('Invalid order type. Must be "buy" or "sell".')
            if not symbol:
                raise ValueError('Symbol is required.')
            if not quantity or quantity <= 0:
                raise ValueError('Quantity must be a positive number.')
            if not price or price <= 0:
                raise ValueError('Price must be a positive number.')
            
            # insert order into database
            timestamp = int(time.time())
            self.cursor.execute('INSERT INTO orders (order_type, symbol, quantity, price, timestamp) VALUES (?, ?, ?, ?, ?)', 
                                (order_type, symbol, quantity, price, timestamp))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Error creating order: {e}')
            return False

    def schedule_order(self, order_type, symbol, quantity, price, frequency, start_time):
        """
        Schedules a recurring buy or sell order with the given parameters.
        """
        try:
            # validate input
            if not frequency or frequency <= 0:
                raise ValueError('Frequency must be a positive number.')
            if not start_time:
                raise ValueError('Start time is required.')

            # create initial order
            self.create_order(order_type, symbol, quantity, price)

            # insert scheduled order into database
            self.cursor.execute('INSERT INTO scheduled_orders (order_type, symbol, quantity, price, frequency, start_time) VALUES (?, ?, ?, ?, ?, ?)', 
                                (order_type, symbol, quantity, price, frequency, start_time))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Error scheduling order: {e}')
            return False

    def cancel_order(self, order_id):
        """
        Cancels the order with the given ID.
        """
        try:
            # delete order from database
            self.cursor.execute('DELETE FROM orders WHERE id=?', (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Error canceling order: {e}')
            return False

    def get_scheduled_orders(self):
        """
        Returns a list of all scheduled orders.
        """
        try:
            self.cursor.execute('SELECT * FROM scheduled_orders')
            return self.cursor.fetchall()
        except Exception as e:
            print(f'Error getting scheduled orders: {e}')
            return []

    def run_scheduled_orders(self):
        """
        Runs all scheduled orders that are due.
        """
        try:
            timestamp = int(time.time())
            self.cursor.execute('SELECT * FROM scheduled_orders WHERE start_time <= ? AND (? - start_time) % frequency = 0', 
                                (timestamp, timestamp))
            orders = self.cursor.fetchall()

            for order in orders:
                self.create_order(order[1], order[2], order[3], order[4])

            return True
        except Exception as e:
            print(f'Error running scheduled orders: {e}')
            return False

    def __del__(self):
        self.cursor.close()
        self.conn.close()
