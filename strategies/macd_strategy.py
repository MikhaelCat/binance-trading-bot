import pandas as pd
import ta
from strategies.base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        super().__init__("MACD Strategy")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def get_required_indicators(self) -> list:
        return ['macd', 'macd_signal', 'macd_hist']
    
    def analyze(self, data: pd.DataFrame) -> dict:
        if len(data) < max(self.fast_period, self.slow_period) + self.signal_period:
            return {'signal': 'HOLD', 'confidence': 0.0, 'details': {}}
        
        # Расчет MACD
        macd_indicator = ta.trend.MACD(
            data['close'],
            window_fast=self.fast_period,
            window_slow=self.slow_period,
            window_sign=self.signal_period
        )
        
        data['macd'] = macd_indicator.macd()
        data['macd_signal'] = macd_indicator.macd_signal()
        data['macd_hist'] = macd_indicator.macd_diff()
        
        current_macd = data['macd'].iloc[-1]
        current_signal = data['macd_signal'].iloc[-1]
        previous_macd = data['macd'].iloc[-2]
        previous_signal = data['macd_signal'].iloc[-2]
        
        # Генерация сигнала
        if (previous_macd <= previous_signal) and (current_macd > current_signal):
            signal = 'BUY'
            confidence = min(abs(current_macd - current_signal) / abs(current_signal), 1.0)
        elif (previous_macd >= previous_signal) and (current_macd < current_signal):
            signal = 'SELL'
            confidence = min(abs(current_macd - current_signal) / abs(current_signal), 1.0)
        else:
            signal = 'HOLD'
            confidence = 0.0
        
        details = {
            'macd': round(current_macd, 4),
            'signal_line': round(current_signal, 4),
            'histogram': round(data['macd_hist'].iloc[-1], 4),
            'price': round(data['close'].iloc[-1], 2)
        }
        
        return {
            'signal': signal,
            'confidence': round(confidence, 2),
            'details': details
        }