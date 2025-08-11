from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from config.settings import settings
from utils.logger import logger

class BinanceClient:
    def __init__(self):
        self.client = Client(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET
        )
    
    def get_klines(self, symbol: str, interval: str, limit: int = 100):
        """Получение свечей"""
        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
            ])
            
            df['close'] = pd.to_numeric(df['close'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error getting klines: {e}")
            return None
    
    def get_balance(self, asset: str) -> float:
        """Получение баланса актива"""
        try:
            balance = self.client.get_asset_balance(asset=asset)
            return float(balance['free'])
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0.0
    
    def create_market_order(self, symbol: str, side: str, quantity: float):
        """Создание рыночного ордера"""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance Order Error: {e.message}")
            return None
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    def create_test_order(self, symbol: str, side: str, quantity: float):
        """Создание тестового ордера"""
        try:
            order = self.client.create_test_order(
                symbol=symbol,
                side=side,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return True
        except Exception as e:
            logger.error(f"Error creating test order: {e}")
            return False