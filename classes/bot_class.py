from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.handler import load_user_context, save_user_context
from handlers.file_handler import clear_file
from handlers.logger import Logger
from classes.question_answer_base import QuestionAnswerBase
import os
import textwrap

logger = Logger('ChatBotLogger').get_logger()

class ChatBot:
    def __init__(self, telegram_token: str, openai_key: str):
        self.telegram_token = telegram_token
        self.openai_key = openai_key
        self.greeting = textwrap.dedent('''\
            Привет, этот бот отвечает на вопросы о POSTHUMAN.
            Ваши вопросы и ответы бота хранятся в отдельном файле
            с вашим юзернеймом и ID чата — контексте.
            Вы можете стереть его, воспользовавшись командой /clear,
            и на сервере весь контекст сотрется, будет пустая история.
        ''')
        
        self.application = (
            Application.builder().token(self.telegram_token).build()
        )
        self.qa_base = QuestionAnswerBase(
            openai_api_key = os.getenv('OPENAI_API_KEY'), 
            word_file_path='documentation.docx'
        )
        self.file_path = lambda name, id: f'contexts/context_{name}_{id}.txt'

    def get_user_name(self, update: Update) -> str:
        return (
            update.message.chat.username 
            or update.message.chat.first_name 
            or 'unknown_user'
        ).strip()

    def start(self):
        logger.info('Запуск бота...')

        self.application.add_handler(
            CommandHandler('start', self.handle_start)
        )
        self.application.add_handler(
            CommandHandler('clear', self.handle_clear)
        )
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, 
                self.handle_message
            )
        )

        # Запуск бота
        self.application.run_polling()

    async def handle_start(
            self, update: Update, 
            context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id
            context.user_data['context_memory'] = (
                load_user_context(user_name, chat_id)
            )
            await update.message.reply_text(self.greeting)
        except Exception as e:
            logger.error(f'Ошибка в обработчике /start: {e}')

    async def handle_clear(
            self, update: Update, 
            context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id
            clear_file(self.file_path(user_name, chat_id))
            context.user_data['context_memory'] = []
            logger.info('Контекст очищен')
            await update.message.reply_text('Контекст очищен.')
        except Exception as e:
            logger.error(f'Ошибка при очистке контекста: {e}')

    async def handle_message(
            self, update: Update, 
            context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        try:
            user_message = update.message.text
            logger.info(f'Получено сообщение: "{user_message}" '
                        f'от пользователя {self.get_user_name}')
            if 'context_memory' not in context.user_data:
                context.user_data['context_memory'] = []
            response = self.qa_base.search_in_word_document(user_message)
            if response:
                logger.info(f'Найден ответ: "{response}"')
                await update.message.reply_text(response)

                # Update and save the context
                context.user_data['context_memory'].append({
                    'role': 'user',
                    'content': user_message
                })
                context.user_data['context_memory'].append({
                    'role': 'assistant',
                    'content': response
                })

                # Save the context to file
                user_name = self.get_user_name(update)
                chat_id = update.message.chat_id
                save_user_context(
                    user_name, chat_id, context.user_data['context_memory']
                )
            else:
                logger.info('Не удалось найти верный ответ в документации.')
                await update.message.reply_text(
                    'Извините, я не могу найти ответ на ваш вопрос.'
                )

        except Exception as e:
            logger.error(f'Ошибка в обработчике сообщений: {e}')
            await update.message.reply_text(
                'Произошла ошибка при обработке вашего сообщения'
                )
