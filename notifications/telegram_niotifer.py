import requests
from config.settings import settings
from utils.logger import logger

class TelegramNotifier:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def send_message(self, message: str):
        """Отправка сообщения в Telegram"""
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"Telegram API error: {response.text}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")