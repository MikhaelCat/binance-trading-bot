import time
from strategies.macd_strategy import MACDStrategy  
from strategies.bollinger_strategy import BollingerBandsStrategy 
from exchanges.binance_client import BinanceClient
from notifications.telegram_notifier import TelegramNotifier
from strategies.rsi_strategy import RSIStrategy
from config.settings import settings
from utils.logger import logger
from strategies.ml_strategy import MLStrategy
from ml.prediction.predictor import PricePredictor

class TradingBot:
    def __init__(self):
        self.binance = BinanceClient()
        self.notifier = TelegramNotifier()
        self.strategy = RSIStrategy()
        self.symbol = settings.SYMBOL
        self.quantity = settings.TRADE_QUANTITY
        self.interval = settings.BINANCE_INTERVAL
        self.ml_predictor = PricePredictor()
        self.ml_strategy = MLStrategy()

        self.strategies = {
            'RSI': self.strategy,
            'MACD': MACDStrategy(), 
            'Bollinger': BollingerBandsStrategy(), 
            'ML': self.ml_strategy
        }
        
        logger.info("Trading Bot initialized")
        self.notifier.send_message("🟢 Бот запущен!")
    
    def get_market_data(self):
        """Получение рыночных данных"""
        return self.binance.get_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=100
        )
    
    def check_position(self):
        """Проверка наличия позиции"""
        asset = self.symbol.replace('USDT', '')
        balance = self.binance.get_balance(asset)
        return balance > 0.0001
    
    def execute_trade(self, signal: str):
        """Выполнение сделки"""
        if signal == 'BUY':
            result = self.binance.create_test_order(
                symbol=self.symbol,
                side='BUY',
                quantity=self.quantity
            )
            if result:
                message = f"✅ ТЕСТОВАЯ ПОКУПКА\nСимвол: {self.symbol}\nКоличество: {self.quantity}"
                self.notifier.send_message(message)
                logger.info(message)
        elif signal == 'SELL':
            result = self.binance.create_test_order(
                symbol=self.symbol,
                side='SELL',
                quantity=self.quantity
            )
            if result:
                message = f"✅ ТЕСТОВАЯ ПРОДАЖА\nСимвол: {self.symbol}\nКоличество: {self.quantity}"
                self.notifier.send_message(message)
                logger.info(message)
    
    def run_strategy(self):
        """Запуск стратегии"""
        try:
            # Получение данных
            data = self.get_market_data()
            if data is None or data.empty:
                return
            
            # Анализ стратегии
            analysis = self.strategy.analyze(data)
            signal = analysis['signal']
            confidence = analysis['confidence']
            details = analysis['details']
            
            # Отправка уведомления о анализе
            message = (
                f"📊 Анализ {self.symbol}\n"
                f"Цена: ${details.get('price', 0)}\n"
                f"RSI: {details.get('rsi', 0)}\n"
                f"Сигнал: {signal} (уверенность: {confidence*100:.0f}%)"
            )
            self.notifier.send_message(message)
            
            # Выполнение сделки (только для тестирования)
            if signal in ['BUY', 'SELL']:
                has_position = self.check_position()
                
                # Логика предотвращения дублирования сделок
                if (signal == 'BUY' and not has_position) or (signal == 'SELL' and has_position):
                    self.execute_trade(signal)
                else:
                    logger.info(f"Сигнал {signal} проигнорирован: позиция уже открыта/закрыта")

            # Анализ всех стратегий
            signals = {}
            for name, strategy in self.strategies.items():
                analysis = strategy.analyze(data)
                signals[name] = analysis
                
                # Отправка уведомления о ML предсказании
                if name == 'ML' and analysis['signal'] != 'HOLD':
                    ml_message = (
                        f"🤖 ML Предсказание для {self.symbol}\n"
                        f"Текущая цена: ${analysis['details']['current_price']}\n"
                        f"Прогноз: ${analysis['details']['predicted_price']}\n"
                        f"Изменение: {analysis['details']['change_percent']}%\n"
                        f"Сигнал: {analysis['signal']} ({analysis['confidence']*100:.0f}% уверенность)"
                    )
                    self.notifier.send_message(ml_message)
            
            # Комбинированный сигнал 
            combined_signal = self.combine_signals(signals)
            
        except Exception as e:
            error_msg = f"❌ Ошибка в стратегии: {e}"
            logger.error(error_msg)
            self.notifier.send_message(error_msg)
    
    def start(self):
        """Запуск бота"""
        logger.info("Starting trading bot...")
        while True:
            try:
                self.run_strategy()
                time.sleep(60)  # Проверка каждую минуту
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                self.notifier.send_message("🔴 Бот остановлен!")
                break
            except Exception as e:
                error_msg = f"❌ Критическая ошибка: {e}"
                logger.error(error_msg)
                self.notifier.send_message(error_msg)
                time.sleep(60)

    def combine_signals(self, signals):
        """Комбинирование сигналов от разных стратегий"""
        buy_votes = 0
        sell_votes = 0
        total_confidence = 0
        
        for strategy_name, signal_data in signals.items():
            signal = signal_data['signal']
            confidence = signal_data['confidence']
            
            if 'BUY' in signal:
                buy_votes += 1
                total_confidence += confidence
            elif 'SELL' in signal:
                sell_votes += 1
                total_confidence += confidence
        
        if buy_votes > sell_votes and buy_votes >= 2:
            return 'BUY'
        elif sell_votes > buy_votes and sell_votes >= 2:
            return 'SELL'
        else:
            return 'HOLD'
