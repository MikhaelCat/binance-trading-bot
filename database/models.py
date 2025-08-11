from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # BUY/SELL
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='executed')  # executed, failed, cancelled
    order_id = Column(String)
    strategy = Column(String)
    profit = Column(Float)
    commission = Column(Float)

class Signal(Base):
    __tablename__ = 'signals'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    strategy = Column(String, nullable=False)
    signal_type = Column(String, nullable=False)  # BUY/SELL/HOLD
    confidence = Column(Float)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    executed = Column(Boolean, default=False)

class Balance(Base):
    __tablename__ = 'balances'
    
    id = Column(Integer, primary_key=True)
    asset = Column(String, nullable=False)
    free = Column(Float, nullable=False)
    locked = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class BacktestResult(Base):
    __tablename__ = 'backtest_results'
    
    id = Column(Integer, primary_key=True)
    strategy = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_trades = Column(Integer)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    total_return = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)