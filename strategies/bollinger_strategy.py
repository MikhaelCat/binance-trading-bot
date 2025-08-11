import pandas as pd
import ta
from strategies.base_strategy import BaseStrategy

class BollingerBandsStrategy(BaseStrategy):
    def __init__(self, window: int = 20, num_std: float = 2.0):
        super().__init__("Bollinger Bands Strategy")
        self.window = window
        self.num_std = num_std
    
    def get_required_indicators(self) -> list:
        return ['bb_upper', 'bb_lower', 'bb_middle']
    
    def analyze(self, data: pd.DataFrame) -> dict:
        if len(data) < self.window:
            return {'signal': 'HOLD', 'confidence': 0.0, 'details': {}}
        
        # Расчет полос Боллинджера
        bb_indicator = ta.volatility.BollingerBands(
            data['close'],
            window=self.window,
            window_dev=self.num_std
        )
        
        data['bb_upper'] = bb_indicator.bollinger_hband()
        data['bb_lower'] = bb_indicator.bollinger_lband()
        data['bb_middle'] = bb_indicator.bollinger_mavg()
        
        current_price = data['close'].iloc[-1]
        upper_band = data['bb_upper'].iloc[-1]
        lower_band = data['bb_lower'].iloc[-1]
        middle_band = data['bb_middle'].iloc[-1]
        
        # Генерация сигнала
        if current_price <= lower_band:
            signal = 'BUY'
            confidence = (lower_band - current_price) / (upper_band - lower_band)
        elif current_price >= upper_band:
            signal = 'SELL'
            confidence = (current_price - upper_band) / (upper_band - lower_band)
        else:
            signal = 'HOLD'
            confidence = 0.0
        
        details = {
            'price': round(current_price, 2),
            'upper_band': round(upper_band, 2),
            'lower_band': round(lower_band, 2),
            'middle_band': round(middle_band, 2)
        }
        
        return {
            'signal': signal,
            'confidence': round(confidence, 2),
            'details': details
        }