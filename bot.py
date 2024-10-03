from dotenv import load_dotenv
import os
from classes.bot_class import ChatBot
from handlers.logger import Logger

# Создаем логгер для главного файла
logger = Logger('MainLogger').get_logger()

# Загрузка переменных окружения из файла .env
load_dotenv()

def main():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
        raise ValueError(
            'Не удалось загрузить TELEGRAM_BOT_TOKEN или OPENAI_API_KEY.'
        )
    
    # Создаем и запускаем экземпляр бота
    chatbot = ChatBot(TELEGRAM_BOT_TOKEN, OPENAI_API_KEY)
    chatbot.start()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Ошибка при загрузке конфигурации или запуске бота: {e}')
