from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def analyze(self, data: pd.DataFrame) -> dict:
        """Анализ данных и возврат сигнала
        Возвращает: {'signal': 'BUY'|'SELL'|'HOLD', 'confidence': float, 'details': dict}
        """
        pass
    
    @abstractmethod
    def get_required_indicators(self) -> list:
        

        pass
