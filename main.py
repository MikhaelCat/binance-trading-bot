import asyncio
import uvicorn
from core.bot import TradingBot
from web.app import app
from config.settings import settings
from database.migrations.init_db import init_database
import threading

def run_bot():
    """Запуск торгового бота"""
    bot = TradingBot()
    bot.start()

def run_web():
    """Запуск веб-интерфейса"""
    uvicorn.run(
        "web.app:app",
        host=settings.WEB_HOST,
        port=settings.WEB_PORT,
        reload=False
    )

if __name__ == "__main__":
    # Инициализация базы данных
    init_database()
    
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запуск веб-сервера в основном потоке
    run_web()