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

        # Разные форматтеры для разных логгеров
        if logger_name == 'ChatBotLogger':
            formatter = logging.Formatter(f"{Fore.BLUE}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Style.RESET_ALL}")
        elif logger_name == 'FileHandlerLogger':
            formatter = logging.Formatter(f"{Fore.GREEN}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Style.RESET_ALL}")
        elif logger_name == 'QuestionAnswerBaseLogger':
            formatter = logging.Formatter(f"{Fore.YELLOW}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Style.RESET_ALL}")    
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Применяем форматтер к обработчику
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
