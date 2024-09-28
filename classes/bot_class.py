from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.handler import load_user_context, save_user_context
import openai
from handlers.logger import Logger
from handlers.api_handler import get_openai_response, preprocess_prompt
from classes.question_answer_base import QuestionAnswerBase

logger = Logger('ChatBotLogger').get_logger()
qa_base = QuestionAnswerBase(file_path='data.txt')

class ChatBot:
    def __init__(self, telegram_token: str, openai_key: str):
        self.telegram_token = telegram_token
        self.openai_key = openai_key
        openai.api_key = self.openai_key
        self.application = Application.builder().token(self.telegram_token).build()

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

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user_message = update.message.text
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id

            # Загружаем контекст пользователя, если он еще не загружен
            if 'context_memory' not in context.user_data:
                context.user_data['context_memory'] = load_user_context(user_name, chat_id)

            # Получаем текущий контекст пользователя
            context_memory = context.user_data['context_memory']

            # Добавляем оригинальный вопрос пользователя в контекст
            context_memory.append({"role": "user", "content": user_message})

            # Попытка найти похожий вопрос в локальном файле
            response = qa_base.search_approximate_answer(user_message)
            found_in_file = False  # Флаг для отслеживания источника ответа

            if response:
                logger.info("Ответ найден в локальном файле.")
                found_in_file = True
            else:
                # Если ответ не найден в локальном файле, обрабатываем сообщение и обращаемся к OpenAI
                processed_message = preprocess_prompt(user_message)
                context_memory[-1]["content"] = processed_message  # Обновляем последний вопрос в контексте
                response = get_openai_response(context_memory)

            if response:
                # Добавляем ответ в контекст
                context_memory.append({"role": "assistant", "content": response})

                # Сохраняем контекст
                save_user_context(user_name, chat_id, context_memory)

                # Отправляем ответ пользователю
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("Не удалось получить ответ.")

            # Логирование источника ответа
            if found_in_file:
                logger.info(f"Ответ для '{user_message}' взят из локального файла.")
            else:
                logger.info(f"Ответ для '{user_message}' сгенерирован OpenAI.")
                
        except Exception as e:
            logger.error(f"Ошибка в обработчике сообщений: {e}")
            await update.message.reply_text("Произошла ошибка при обработке вашего сообщения.")
