import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    # Маппинг цветов для разных логгеров
    LOG_COLORS = {
        'ChatBotLogger': Fore.BLUE,
        'FileHandlerLogger': Fore.GREEN,
        'QuestionAnswerBaseLogger': Fore.YELLOW
    }

    def __init__(self, logger_name, fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        super().__init__(fmt)
        self.logger_name = logger_name
        self.base_color = self.LOG_COLORS.get(logger_name, Fore.WHITE)

    def format(self, record):
        # Добавляем цвет для ERROR уровня
        if record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        else:
            record.msg = f"{self.base_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

class Logger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        
        # Используем наш кастомный форматтер
        formatter = ColoredFormatter(logger_name)
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
