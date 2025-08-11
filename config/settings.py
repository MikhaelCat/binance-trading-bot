import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Binance
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Trading
    SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
    TRADE_QUANTITY = float(os.getenv("TRADE_QUANTITY", "0.001"))
    INTERVAL = os.getenv("INTERVAL", "15m")
    STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", "2.0"))
    TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", "5.0"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading_bot.db")
    
    # Web
    WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT = int(os.getenv("WEB_PORT", "8000"))
    
    # Risk Management
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "100"))
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.01"))
    
    # Преобразование интервала для Binance
    INTERVAL_MAP = {
        '1m': '1m',
        '5m': '5m',
        '15m': '15m',
        '30m': '30m',
        '1h': '1h',
        '4h': '4h',
        '1d': '1d'
    }
    
    BINANCE_INTERVAL = INTERVAL_MAP.get(INTERVAL, '15m')

settings = Settings()