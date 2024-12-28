from handlers.handler import load_user_context, save_user_context
from handlers.file_handler import remove_context_file
from handlers.logger import Logger

logger = Logger('UserContextLogger').get_logger()

class UserContext:
    def __init__(self, user_name, chat_id, documentation_text, user_data):
        self.user_name = user_name
        self.chat_id = chat_id
        self.documentation_text = documentation_text
        self.user_data = user_data
        self.file_path = lambda name, id: f'contexts/context_{name}_{id}.txt'

        # Инициализируем context_memory из user_data или загружаем из файла
        self.context_memory = self.user_data.get('context_memory', [])
        if not self.context_memory:
            self.load_context()
            self.user_data['context_memory'] = self.context_memory
        self.ensure_system_message()

    def load_context(self):
        try:
            self.context_memory = load_user_context(self.user_name, self.chat_id)
            if not self.context_memory:
                self.context_memory = []
                logger.info(f'Создан новый контекст для пользователя {self.user_name}')
            else:
                logger.info(f'Контекст для пользователя {self.user_name} загружен')
        except Exception as e:
            logger.error(f'Ошибка при загрузке контекста: {e}')
            self.context_memory = []

    def update_context(self, message):
        self.context_memory.append(message)
        self.user_data['context_memory'] = self.context_memory
        logger.info(f'Контекст обновлён: добавлено от {message["role"]}')
        logger.info(f'Добавленное сообщение: {message}')

    def save_context(self, n_messages=None):
        try:
            if n_messages is not None:
                context_to_save = self.context_memory[-n_messages:]
            else:
                context_to_save = self.context_memory
            save_user_context(self.user_name, self.chat_id, context_to_save)
            self.user_data['context_memory'] = self.context_memory
            logger.info(f'Контекст для пользователя {self.user_name} сохранен')
        except Exception as e:
            logger.error(f'Ошибка при сохранении контекста: {e}')

    def clear_context(self):
        try:
            remove_context_file(self.file_path(self.user_name, self.chat_id))
            self.context_memory = []
            self.user_data['context_memory'] = self.context_memory
            logger.info(f'Контекст для пользователя {self.user_name} очищен')
        except Exception as e:
            logger.error(f'Ошибка при очистке контекста: {e}')
        

    def get_context(self):
        return self.context_memory

    def ensure_system_message(self):
        if not any(message['role'] == 'system' for message in self.context_memory):
            system_message = {
                'role': 'system',
                'content': f"Программа POSTHUMAN:\n{self.documentation_text}"
            }
            self.context_memory.insert(0, system_message)
            logger.info('Добавлено системное сообщение в контекст.')
