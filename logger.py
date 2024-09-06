import logging
import colorlog



class Logger1():
    def __init__(self) -> None:
        pass

class Logger():
    def __init__(self, name: str, level=logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

# Настройка форматтера с цветами
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s: %(message)s",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'bold_cyan',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

    # Создание и настройка консольного хендлера
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
       
    def get_logger(self):
        return self.logger

logger1 = Logger('my_logger', logging.DEBUG).get_logger()

class Logger2():
     def __init__(self, name: str, *args, level=logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatstring = ' - '.join(args) if args else '%(message)s'
        
        log_colors = {
            'DEBUG': 'purple',
            'INFO': 'bold_green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        color_formatter = colorlog.ColoredFormatter(
            f'%(log_color)s{formatstring}', log_colors=log_colors
        )
        console_handler.setFormatter(color_formatter)

        self.logger.addHandler(console_handler)

     def get_logger(self):
         return self.logger


logger2 = Logger2(
    '%(levelname)s',__name__,  
    '%(funcName)s', 
    '%(asctime)s', 
    '%(message)s',
    ).get_logger()

