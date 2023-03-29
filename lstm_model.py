import numpy as np
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

class LSTMModel:
    def __init__(self, input_shape=(1, 1), lstm_units=64, dense_units=1, learning_rate=0.001):
        self.model = Sequential()
        self.model.add(LSTM(lstm_units, input_shape=input_shape))
        self.model.add(Dense(dense_units))
        self.optimizer = Adam(lr=learning_rate)
        self.model.compile(loss='mean_squared_error', optimizer=self.optimizer)

    def train(self, x_train, y_train, epochs=1, batch_size=1, verbose=0):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, x):
        return self.model.predict(x)

def create_lstm_model(input_shape, lstm_units, dense_units, learning_rate):
    return LSTMModel(input_shape, lstm_units, dense_units, learning_rate)
