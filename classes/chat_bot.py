from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.file_handler import load_text_from_word
from handlers.logger import Logger
from classes.user_context import UserContext
from classes.question_answer_base import QuestionAnswerBase
import textwrap

logger = Logger('ChatBotLogger').get_logger()

class ChatBot:
    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.greeting = textwrap.dedent('''\
            Привет, этот бот отвечает на вопросы о POSTHUMAN.
            Ваши вопросы и ответы бота хранятся в отдельном файле
            с вашим юзернеймом и ID чата — контексте.
            Вы можете стереть его, воспользовавшись командой /clear,
            и на сервере весь контекст сотрется, будет пустая история.
        ''')
        self.word_file_path ='ОПИСАНИЕ ВАЛИДАТОРА POSTHUMAN.docx'
        
        self.application = (
            Application.builder().token(self.telegram_token).build()
        )
        self.documentation_text = load_text_from_word(self.word_file_path)
        
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
            user_context = UserContext(user_name, chat_id, self.documentation_text, context.user_data)
            user_context.clear_context()            
            logger.info(f'Контекст очищен для {user_name}')
            await update.message.reply_text('Контекст очищен.')
        except Exception as e:
            logger.error(f'Ошибка при очистке контекста: {e}')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user_name = self.get_user_name(update)
            chat_id = update.message.chat_id

            # Передаем context.user_data в UserContext
            user_context = UserContext(user_name, chat_id, self.documentation_text, context.user_data)

            # Получаем сообщение пользователя
            user_message = update.message.text
            logger.info(f'Новое сообщение: "{user_message}" от пользователя {user_name}')

            # Проверяем, есть ли такое сообщение в контексте
            if not any(message['content'] == user_message for message in user_context.get_context()):
                # Добавляем сообщение пользователя в контекст
                user_context.update_context({
                    'role': 'user',
                    'content': f'{user_message}, ответь только по программе POSTHUMAN или найди ответ в контексте блокчейна'
                })

            # Создаем экземпляр QuestionAnswerBase, передавая user_context
            qa_base = QuestionAnswerBase(user_context, self.word_file_path)

            # Отправляем запрос в OpenAI
            response = qa_base.query_openai()

            if response:
                logger.info(f'Найден ответ: "{response}"')
                await update.message.reply_text(response)

                # Добавляем ответ ассистента в контекст
                user_context.update_context({
                    'role': 'assistant',
                    'content': response
                })

                # Сохраняем контекст (можно сохранить последние два сообщения)
                user_context.save_context(n_messages=2)
            else:
                logger.info('Не удалось найти верный ответ в документации.')
                await update.message.reply_text(f'Извините, {user_name}, вам нужно стереть контекст командой /clear и задать вопрос повторно')

        except Exception as e:
            logger.error(f'Ошибка в обработчике сообщений: {e}')
            await update.message.reply_text('Произошла ошибка при обработке вашего сообщения.')
