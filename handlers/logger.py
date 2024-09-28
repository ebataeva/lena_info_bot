import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()

        # Маппинг для цветовой схемы на основе имени логгера
        logger_color_mapping = {
            'ChatBotLogger': Fore.BLUE,
            'FileHandlerLogger': Fore.GREEN,
            'QuestionAnswerBaseLogger': Fore.YELLOW
        }
        
        # Получаем цвет из маппинга или используем белый цвет по умолчанию
        self.base_color = logger_color_mapping.get(logger_name, Fore.WHITE)

        # Определяем базовый форматтер
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Устанавливаем форматтер для обработчика
        console_handler.setFormatter(self.formatter)

        # Добавляем обработчик к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

    def _format_message(self, record):
        # Если уровень логирования ERROR, используем красный цвет
        if record.levelno == logging.ERROR:
            return f"{Fore.RED}{self.formatter.format(record)}{Style.RESET_ALL}"
        else:
            return f"{self.base_color}{self.formatter.format(record)}{Style.RESET_ALL}"

    # Кастомный emit метод для логгера
    def _log_with_color(self, level, message, *args, **kwargs):
        record = self.logger.makeRecord(self.logger.name, level, fn=None, lno=0, msg=message, args=args, exc_info=kwargs.get('exc_info'))
        colored_message = self._format_message(record)
        print(colored_message)  # Печатаем форматированное сообщение

    # Методы для цветного логирования
    def debug(self, message, *args, **kwargs):
        self._log_with_color(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log_with_color(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log_with_color(logging.WARNING, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log_with_color(logging.ERROR, message, *args, **kwargs)
