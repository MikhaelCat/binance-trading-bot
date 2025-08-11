import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import joblib

class LSTMPricePredictor:
    def __init__(self, sequence_length=60, epochs=50, batch_size=32):
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = MinMaxScaler()
        self._build_model()
    
    def _build_model(self):
        """Построение LSTM модели"""
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1)
        ])
        
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mean_squared_error',
            metrics=['mae']
        )
    
    def prepare_data(self, data):
        """Подготовка данных для обучения"""
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y
    
    def train(self, data):
        """Обучение модели"""
        X, y = self.prepare_data(data)
        
        history = self.model.fit(
            X, y,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.1,
            verbose=1
        )
        
        return history
    
    def predict(self, data):
        """Предсказание"""
        scaled_data = self.scaler.transform(data[-self.sequence_length:].reshape(-1, 1))
        X = np.array([scaled_data])
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        prediction = self.model.predict(X, verbose=0)
        return self.scaler.inverse_transform(prediction)[0, 0]
    
    def save_model(self, filepath):
        """Сохранение модели"""
        self.model.save(f"{filepath}_model.h5")
        joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
    
    def load_model(self, filepath):
        """Загрузка модели"""
        from tensorflow.keras.models import load_model
        self.model = load_model(f"{filepath}_model.h5")
        self.scaler = joblib.load(f"{filepath}_scaler.pkl")