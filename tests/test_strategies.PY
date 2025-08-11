import pandas as pd
from strategies.rsi_strategy import RSIStrategy

def test_rsi_strategy():
    # Создаем тестовые данные
    data = pd.DataFrame({
        'close': [40000, 39000, 38000, 37000, 36000, 37000, 38000, 39000, 40000, 41000] * 2
    })
    
    strategy = RSIStrategy()
    result = strategy.analyze(data)
    
    assert 'signal' in result
    assert result['signal'] in ['BUY', 'SELL', 'HOLD']
    print("RSI Strategy test passed!")

if __name__ == "__main__":
    test_rsi_strategy()