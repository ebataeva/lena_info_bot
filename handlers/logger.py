import logging
from colorama import Fore, Style, init
import inspect  # Для получения имени вызываемого метода

# Initialize colorama
init(autoreset=True)

# Словарь с цветами для различных логгеров
LOG_COLORS = {
    'ChatBotLogger': Fore.BLUE,
    'FileHandlerLogger': Fore.GREEN,
    'QuestionAnswerBaseLogger': Fore.YELLOW,
    'HandlerLogger': Fore.MAGENTA,
    'APIHandlerLogger': Fore.CYAN,
    'UserContextLogger': Fore.MAGENTA,
    'MainLogger': Fore.WHITE  # Цвет по умолчанию
}

# Кастомный форматтер для логирования с цветами
class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        super().__init__(fmt)

    def format(self, record):
        log_color = LOG_COLORS.get(record.name, Fore.WHITE)
        if record.levelno == logging.ERROR:
            log_color = Fore.RED
        current_method = inspect.stack()[8].function
        # Форматируем сообщение с цветами и добавляем имя метода
        record.msg = f"{log_color}[{current_method}] {record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Класс Logger для создания логгеров
class Logger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        
        # Используем наш кастомный форматтер
        formatter = ColoredFormatter()
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
