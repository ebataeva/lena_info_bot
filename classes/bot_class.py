from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.handler import load_user_context, save_user_context
from handlers.file_handler import remove_context_file
from handlers.logger import Logger
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
        
        self.application = (
            Application.builder().token(self.telegram_token).build()
        )
        self.file_path = lambda name, id: f'contexts/context_{name}_{id}.txt'
        self.user_name = None
        self.chat_id = None
        self.context_data = {}
        self.context_memory = []
        
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
            remove_context_file(self.file_path(user_name, chat_id))
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
            # Инициализируем имя пользователя и ID чата
            self.user_name = self.get_user_name(update)
            self.chat_id = update.message.chat_id
            self.context_data = context.user_data  # Упрощаем доступ к контексту пользователя
            self.context_memory = self.context_data.get('context_memory', [])
            
            # Загрузка контекста из файла, если он не был загружен
            if not self.context_memory:
                logger.info(f'Загрузка контекста для пользователя {self.user_name}')
                self.context_memory = load_user_context(self.user_name, self.chat_id)
                self.context_data['context_memory'] = self.context_memory

            # Получаем сообщение пользователя
            user_message = update.message.text
            logger.info(f'Новое сообщение: "{user_message}" от пользователя {self.user_name}')
            
            if not any(message['content'] == user_message for message in self.context_memory):
                self.context_memory.append({
                    'role': 'user',
                    'content': user_message
                })

            # Создаем экземпляр класса для поиска в документации и отправки запроса
            qa_base = QuestionAnswerBase(self.context_memory)
            
            # Отправляем запрос в OpenAI с контекстом
            response = qa_base.query_openai()

            # Если ответ найден
            if response:
                logger.info(f'Найден ответ: "{response}"')
                await update.message.reply_text(response)

                # Обновляем контекст с ответом
                self.context_memory.append({
                    'role': 'assistant',
                    'content': response
                })

                # Сохраняем контекст пользователя в файл
                save_user_context(self.user_name, self.chat_id, self.context_memory[-2:])
            
            else:
                logger.info('Не удалось найти верный ответ в документации.')
                await update.message.reply_text(f'Извините, {self.user_name}, я не могу найти ответ на ваш вопрос.')

        except Exception as e:
            logger.error(f'Ошибка в обработчике сообщений: {e}')
            await update.message.reply_text('Произошла ошибка при обработке вашего сообщения.')

