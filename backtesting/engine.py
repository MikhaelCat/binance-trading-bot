import pandas as pd
import numpy as np
from typing import List, Dict
from strategies.base_strategy import BaseStrategy
from database.models import BacktestResult

class BacktestEngine:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.initial_capital = 10000
        self.current_capital = self.initial_capital
        self.positions = []
        self.trades = []
        
    def run(self, strategy: BaseStrategy, symbol: str = "BTCUSDT") -> Dict:
        """Запуск бэктеста"""
        results = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'win_rate': 0,
            'profit_factor': 0
        }
        
        equity_curve = [self.initial_capital]
        
        for i in range(len(self.data)):
            if i < 20:  
                continue
                
            # Анализ текущего состояния
            current_data = self.data.iloc[:i+1].copy()
            analysis = strategy.analyze(current_data)
            
            current_price = self.data.iloc[i]['close']
            
            # Имитация торговли
            if analysis['signal'] == 'BUY' and len(self.positions) == 0:
                # Открытие позиции
                position_size = self.current_capital * 0.1 / current_price
                self.positions.append({
                    'entry_price': current_price,
                    'size': position_size,
                    'entry_time': self.data.iloc[i]['timestamp']
                })
                
            elif analysis['signal'] == 'SELL' and len(self.positions) > 0:
                # Закрытие позиции
                position = self.positions.pop()
                pnl = (current_price - position['entry_price']) * position['size']
                self.current_capital += pnl
                self.trades.append({
                    'entry_price': position['entry_price'],
                    'exit_price': current_price,
                    'pnl': pnl,
                    'timestamp': self.data.iloc[i]['timestamp']
                })
            
            equity_curve.append(self.current_capital)
        
        
        if len(self.trades) > 0:
            winning_trades = [t for t in self.trades if t['pnl'] > 0]
            losing_trades = [t for t in self.trades if t['pnl'] < 0]
            
            total_pnl = sum([t['pnl'] for t in self.trades])
            win_rate = len(winning_trades) / len(self.trades) if self.trades else 0
            
            winning_amount = sum([t['pnl'] for t in winning_trades])
            losing_amount = abs(sum([t['pnl'] for t in losing_trades]))
            profit_factor = winning_amount / losing_amount if losing_amount > 0 else float('inf')
            
            # Расчет максимальной просадки
            equity_series = pd.Series(equity_curve)
            rolling_max = equity_series.expanding().max()
            drawdown = (equity_series - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            results.update({
                'total_trades': len(self.trades),
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'total_pnl': total_pnl,
                'max_drawdown': abs(max_drawdown),
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_return': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
            })
        

        return results
