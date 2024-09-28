import logging
import colorlog

class Logger:
    def __init__(self, name: str, level=logging.DEBUG):
        # Создаем базовый логгер с заданным именем
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Настраиваем цветной форматтер для консольного вывода
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'bold_cyan',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Создаем и настраиваем консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру, если его нет
        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
