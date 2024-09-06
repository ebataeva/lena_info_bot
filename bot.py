from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes)
import openai
from dotenv import load_dotenv
import os
from logger import logger1, logger2
from file_handler import *
from handler import *

# Загрузка переменных окружения из файла .env
load_dotenv()

# Вставьте сюда токен Telegram-бота и API-ключ OpenAI из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY 

def main() -> None:
    # Загрузка контекста из файла
    load_context_from_file()

    # Создаем приложение и передаем ему токен вашего бота
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message)
        )

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
