import pandas as pd
import ta
from strategies.base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, rsi_period: int = 14, rsi_overbought: int = 70, rsi_oversold: int = 30):
        super().__init__("RSI Strategy")
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
    
    def get_required_indicators(self) -> list:
        return ['rsi']
    
    def analyze(self, data: pd.DataFrame) -> dict:
        if len(data) < self.rsi_period:
            return {'signal': 'HOLD', 'confidence': 0.0, 'details': {}}
        
        # Расчет RSI
        rsi_indicator = ta.momentum.RSIIndicator(data['close'], window=self.rsi_period)
        data['rsi'] = rsi_indicator.rsi()
        
        current_rsi = data['rsi'].iloc[-1]
        previous_rsi = data['rsi'].iloc[-2] if len(data) > 1 else current_rsi
        
        # Генерация сигнала
        if current_rsi < self.rsi_oversold and previous_rsi >= self.rsi_oversold:
            signal = 'BUY'
            confidence = (self.rsi_oversold - current_rsi) / self.rsi_oversold
        elif current_rsi > self.rsi_overbought and previous_rsi <= self.rsi_overbought:
            signal = 'SELL'
            confidence = (current_rsi - self.rsi_overbought) / (100 - self.rsi_overbought)
        else:
            signal = 'HOLD'
            confidence = 0.0
        
        details = {
            'rsi': round(current_rsi, 2),
            'price': round(data['close'].iloc[-1], 2)
        }
        
        return {
            'signal': signal,
            'confidence': round(confidence, 2),
            'details': details
        }