from datetime import datetime, timedelta
from typing import Dict, List
from database.models import Trade
from sqlalchemy.orm import Session

class RiskManager:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.daily_loss_limit = 100  # USD
        self.max_position_size = 0.01  # BTC
        self.stop_loss_percent = 2.0
        self.take_profit_percent = 5.0
    
    def check_daily_loss_limit(self) -> bool:
        """Проверка дневного лимита убытков"""
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        daily_trades = self.db.query(Trade).filter(
            Trade.timestamp >= start_of_day,
            Trade.profit < 0
        ).all()
        
        total_loss = sum(abs(trade.profit or 0) for trade in daily_trades)
        return total_loss < self.daily_loss_limit
    
    def calculate_position_size(self, price: float, account_balance: float) -> float:
        """Расчет размера позиции с учетом риска"""
        max_usd_risk = min(account_balance * 0.02, 100)  # 2% от счета или $100
        position_size = max_usd_risk / (price * (self.stop_loss_percent / 100))
        return min(position_size, self.max_position_size)
    
    def should_stop_trading(self) -> bool:
        """Проверка необходимости остановки торговли"""
        return not self.check_daily_loss_limit()
    
    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        """Расчет уровня стоп-лосса"""
        if side == 'BUY':
            return entry_price * (1 - self.stop_loss_percent / 100)
        else:
            return entry_price * (1 + self.stop_loss_percent / 100)
    
    def calculate_take_profit(self, entry_price: float, side: str) -> float:
        """Расчет уровня тейк-профита"""
        if side == 'BUY':
            return entry_price * (1 + self.take_profit_percent / 100)
        else:
            return entry_price * (1 - self.take_profit_percent / 100)