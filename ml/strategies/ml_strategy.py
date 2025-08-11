import pandas as pd
from strategies.base_strategy import BaseStrategy
from ml.prediction.predictor import PricePredictor

class MLStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("ML Strategy")
        self.predictor = PricePredictor()
    
    def get_required_indicators(self) -> list:
        return ['ml_prediction']
    
    def analyze(self, data: pd.DataFrame) -> dict:
        if len(data) < 10:
            return {'signal': 'HOLD', 'confidence': 0.0, 'details': {}}
        
        current_price = data['close'].iloc[-1]
        symbol = "BTCUSDT"  
        
        prediction_result = self.predictor.get_trend_signal(symbol, current_price)
        
        details = {
            'current_price': round(current_price, 2),
            'predicted_price': prediction_result['predicted_price'],
            'change_percent': prediction_result['change_percent'],
            'price': round(current_price, 2)
        }
        
        return {
            'signal': prediction_result['signal'],
            'confidence': prediction_result['confidence'],
            'details': details
        }