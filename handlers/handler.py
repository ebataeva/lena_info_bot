import os
from typing import List, Dict
from handlers.file_handler import load_context_from_file, save_context_to_file
from handlers.logger import Logger

logger = Logger('HandlerLogger').get_logger()

def load_user_context(user_name: str, chat_id: int) -> List[Dict[str, str]]:
    file_path = f'contexts/context_{user_name}_{chat_id}.txt'
    return load_context_from_file(file_path)

def save_user_context(user_name: str, chat_id: int, context_memory: List[Dict[str, str]]):
    file_path = f'contexts/context_{user_name}_{chat_id}.txt'
    save_context_to_file(context_memory, file_path)
