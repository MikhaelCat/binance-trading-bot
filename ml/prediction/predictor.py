import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ml.models.lstm_model import LSTMPricePredictor
from exchanges.binance_client import BinanceClient

class PricePredictor:
    def __init__(self):
        self.lstm_model = LSTMPricePredictor()
        self.binance = BinanceClient()
        self.is_trained = False
    
    def fetch_historical_data(self, symbol, days=30):
        """Получение исторических данных"""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)
        klines = self.binance.client.get_historical_klines(
            symbol=symbol,
            interval='1h',
            start_str=start_timestamp,
            end_str=end_timestamp
        )
        
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        
        df['close'] = pd.to_numeric(df['close'])
        return df['close'].values
    
    def train_model(self, symbol):
        """Обучение модели"""
        print(f"Training model for {symbol}...")
        
        historical_prices = self.fetch_historical_data(symbol, days=90)
        
        self.lstm_model.train(historical_prices)
        self.is_trained = True
        self.lstm_model.save_model(f"models/{symbol.lower()}_lstm")
        
        print("Model training completed!")
    
    def predict_next_price(self, symbol, current_price=None):
        """Предсказание следующей цены"""
        if not self.is_trained:
            try:
                self.lstm_model.load_model(f"models/{symbol.lower()}_lstm")
                self.is_trained = True
            except:
                print("Model not found, training...")
                self.train_model(symbol)
        
        if current_price is None:
            historical_prices = self.fetch_historical_data(symbol, days=3)
        else:
            historical_prices = np.array([current_price])
        
        predicted_price = self.lstm_model.predict(historical_prices)
        return predicted_price
    
    def get_trend_signal(self, symbol, current_price):
        """Получение сигнала тренда"""
        try:
            predicted_price = self.predict_next_price(symbol, current_price)
            change_percent = ((predicted_price - current_price) / current_price) * 100
            
            if change_percent > 1.0:  # Рост более 1%
                signal = 'STRONG_BUY'
                confidence = min(change_percent / 5, 1.0)  
            elif change_percent > 0.5:  
                signal = 'BUY'
                confidence = change_percent / 2
            elif change_percent < -1.0:  # Падение более 1%
                signal = 'STRONG_SELL'
                confidence = min(abs(change_percent) / 5, 1.0)
            elif change_percent < -0.5:  # Падение 0.5-1%
                signal = 'SELL'
                confidence = abs(change_percent) / 2
            else:
                signal = 'HOLD'
                confidence = 0.0
            
            return {
                'signal': signal,
                'confidence': round(confidence, 2),
                'predicted_price': round(predicted_price, 2),
                'current_price': round(current_price, 2),
                'change_percent': round(change_percent, 2)
            }
            
        except Exception as e:
            print(f"Error in trend prediction: {e}")
            return {
                'signal': 'HOLD',
                'confidence': 0.0,
                'predicted_price': current_price,
                'current_price': current_price,
                'change_percent': 0.0
            }