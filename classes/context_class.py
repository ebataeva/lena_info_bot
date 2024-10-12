from typing import List, Dict
from handlers.logger import Logger

logger = Logger('ContextMemory').get_logger()

class ContextHandler:
    def __init__(self) -> None:
        self.context_memory = ''

    def get_context(self) ->  List[Dict[str, str]]:
        logger.info(f'вернули контекст {self.context_memory}')
        return self.context_memory
    
    def add_to_context(self, context_memory: List[Dict[str, str]]) -> None:
        logger.info(f'хотим записать контекст {context_memory}')
        self.context_memory.append(context_memory)
        logger.info(f'вернули контекст с добавочным {self.context_memory}')