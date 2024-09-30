from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.handler import load_user_context, save_user_context
import openai
from handlers.logger import Logger
from handlers.api_handler import get_openai_response, preprocess_prompt
from classes.question_answer_base import QuestionAnswerBase
import os

logger = Logger('ChatBotLogger').get_logger()

class ChatBot:
    def __init__(self, telegram_token: str, openai_key: str):
        self.telegram_token = telegram_token
        self.openai_key = openai_key
        openai.api_key = self.openai_key
        self.application = Application.builder().token(self.telegram_token).build()
        self.qa_base = QuestionAnswerBase(openai_api_key = os.getenv('OPENAI_API_KEY'), word_file_path='documentation.docx')


    def get_user_name(self, update: Update) -> str:
        return (update.message.chat.username or update.message.chat.first_name or 'unknown_user').strip()

    def start(self):
        logger.info("Запуск бота...")
        
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("clear", self.handle_clear))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Запуск бота
        self.application.run_polling()

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id
            context.user_data['context_memory'] = load_user_context(user_name, chat_id)
            await update.message.reply_text('Привет! Начнем новый диалог.')
        except Exception as e:
            logger.error(f"Ошибка в обработчике /start: {e}")

    async def handle_clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id
            file_path = f'contexts/context_{user_name}_{chat_id}.txt'

            # Очистка контекста
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("")

            context.user_data['context_memory'] = []
            await update.message.reply_text("Контекст очищен.")
        except Exception as e:
            logger.error(f"Ошибка при очистке контекста: {e}")

    async def handle_message(self, update, context):
        try:
            user_message = update.message.text
            logger.info(f"Получено сообщение: '{user_message}' от пользователя {update.message.chat_id}")

            # Поиск ответа в Word-документе
            response = self.qa_base.search_in_word_document(user_message)

            # Если найден релевантный ответ
            if response:
                logger.info(f"Найден ответ: '{response}'")
                await update.message.reply_text(response)
            else:
                # Если не удалось найти подходящий ответ
                logger.info("Не удалось найти подходящий ответ в документации.")
                await update.message.reply_text("Извините, я не могу найти ответ на ваш вопрос.")

        except Exception as e:
            logger.error(f"Ошибка в обработчике сообщений: {e}")
            await update.message.reply_text("Произошла ошибка при обработке вашего сообщения.")
