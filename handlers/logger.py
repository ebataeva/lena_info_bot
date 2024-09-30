import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Словарь с цветами для различных логгеров
LOG_COLORS = {
    'ChatBotLogger': Fore.BLUE,
    'FileHandlerLogger': Fore.GREEN,
    'QuestionAnswerBaseLogger': Fore.YELLOW,
    'HandlerLogger': Fore.MAGENTA,
    'APIHandlerLogger': Fore.CYAN,
    'MainLogger': Fore.WHITE  # Цвет по умолчанию
}

# Кастомный форматтер для логирования с цветами
class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        super().__init__(fmt)

    def format(self, record):
        # Получаем базовый цвет логгера или белый по умолчанию
        log_color = LOG_COLORS.get(record.name, Fore.WHITE)

        # Если уровень логирования - ERROR, устанавливаем красный цвет
        if record.levelno == logging.ERROR:
            log_color = Fore.RED

        # Форматируем сообщение с цветами
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
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
