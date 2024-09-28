import os
from typing import List, Dict
import difflib
from handlers.logger import Logger

logger = Logger('FileHandlerLogger').get_logger()

# Функция для загрузки контекста из файла
def load_context_from_file(file_path: str) -> List[Dict[str, str]]:
    logger.info(f"Вызов load_context_from_file с аргументом: file_path = {file_path}")
    context_memory = []
    try:
        logger.info(f"Попытка загрузки контекста из файла: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                if line.startswith("Вопрос:"):
                    context_memory.append({
                        "role": "user",
                        "content": line.replace("Вопрос:", "").strip()
                    })
                elif line.startswith("Ответ:"):
                    context_memory.append({
                        "role": "assistant",
                        "content": line.replace("Ответ:", "").strip()
                    })

        logger.info(f"Контекст успешно загружен. Количество записей: {len(context_memory)}")
    except Exception as e:
        logger.error(f"Ошибка при загрузке контекста из файла: {e}")

    return context_memory

# Функция для записи контекста в файл
def save_context_to_file(context_memory: List[Dict[str, str]], file_path: str, max_length: int = 20, max_file_size: int = 1024 * 10):
    try:
        logger.info(f"Попытка сохранить контекст в файл: {file_path}")
        
        # Оставляем только последние max_length сообщений в контексте
        context_memory = context_memory[-max_length:]
        
        # Сохраняем контекст в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in context_memory:
                if entry['role'] == 'user':
                    file.write(f"Вопрос: {entry['content']}\n")
                elif entry['role'] == 'assistant':
                    file.write(f"Ответ: {entry['content']}\n")
        
        # Логирование для проверки содержимого
        logger.info(f"Контент, записанный в файл: {context_memory}")

        # Проверка размера файла и удаление старых записей, если файл слишком большой
        if os.path.getsize(file_path) > max_file_size:
            logger.info(f"Размер файла {file_path} превысил {max_file_size} байт. Удаляем старые записи.")
            context_memory = context_memory[-max_length//2:]  # Оставляем только половину последних сообщений
            with open(file_path, 'w', encoding='utf-8') as file:
                for entry in context_memory:
                    if entry['role'] == 'user':
                        file.write(f"Вопрос: {entry['content']}\n")
                    elif entry['role'] == 'assistant':
                        file.write(f"Ответ: {entry['content']}\n")
        
        logger.info(f"Контекст успешно сохранен в файл: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при записи в файл: {e}")


# Функция для поиска ответа в контексте
def search_in_file(question: str, context_memory: List[Dict[str, str]]) -> str:
    response = None
    try:
        logger.info(f"Поиск ответа на вопрос: {question}")
        found_question = False
        for entry in context_memory:
            if entry['role'] == 'user' and question.lower() in entry['content'].lower():
                found_question = True
                response_index = context_memory.index(entry) + 1
                if response_index < len(context_memory) and context_memory[response_index]['role'] == 'assistant':
                    response = context_memory[response_index]['content']
                    logger.info("Ответ найден в контексте.")
                    break

        if not response:
            logger.info("Ответ не найден в контексте.")
    except Exception as e:
        logger.error(f"Ошибка при поиске ответа в контексте: {e}")

    return response
