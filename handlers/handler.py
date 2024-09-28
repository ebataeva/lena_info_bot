import os
from typing import List, Dict
from telegram import Update
from telegram.ext import ContextTypes
from handlers.file_handler import load_context_from_file, save_context_to_file, search_in_file
from handlers.api_handler import get_openai_response
from handlers.logger import Logger

logger = Logger('HandlerLogger').get_logger()

def load_user_context(user_name: str, chat_id: int) -> List[Dict[str, str]]:
    file_path = f'contexts/context_{user_name}_{chat_id}.txt'
    return load_context_from_file(file_path)

def save_user_context(user_name: str, chat_id: int, context_memory: List[Dict[str, str]]):
    file_path = f'contexts/context_{user_name}_{chat_id}.txt'
    save_context_to_file(context_memory, file_path)

# Обработчик команды /start
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = (update.message.chat.username or update.message.chat.first_name or 'unknown_user').strip()
    try:
        logger.info("Команда /start получена")
        chat_id = update.message.chat_id
        context.user_data['context_memory'] = load_user_context(user_name or 'unknown_user', chat_id)
        await update.message.reply_text('Приветик! Отправьте мне вопрос, и я постараюсь найти ответ')
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_message = update.message.text
        user_name = update.message.chat.first_name or "Неизвестный пользователь"
        chat_id = update.message.chat_id
        logger.info(f"От {user_name} ({chat_id}) получено сообщение: --- {user_message}")

        # Загружаем контекст пользователя
        if 'context_memory' not in context.user_data:
            context.user_data['context_memory'] = load_user_context(user_name or 'unknown_user', chat_id)

        # Получаем текущий контекст пользователя
        context_memory = context.user_data['context_memory']

        # Сохраняем вопрос пользователя в контексте
        context_memory.append({"role": "user", "content": user_message})
        logger.info("Вопрос добавлен в контекст.")

        # Поиск ответа в контексте
        response = search_in_file(user_message, context_memory)

        if response:
            logger.info("Ответ найден в контексте.")
        else:
            logger.info("Ответ не найден в контексте, запрос к OpenAI...")
            response = get_openai_response(user_message)
            logger.info(f"Ответ получен от OpenAI: {response}")

        # Проверяем, получили ли мы ответ
        if response:
            # Сохраняем ответ бота в контексте
            context_memory.append({"role": "assistant", "content": response})
            logger.info("Ответ добавлен в контекст.")
            
            # Сохраняем вопрос и ответ в файл
            save_user_context(user_name or 'unknown_user', chat_id, context_memory)
            logger.info(f"Контекст для пользователя {chat_id} сохранен в файл.")
            
            await update.message.reply_text(response)
        else:
            logger.error("Не удалось получить ответ от OpenAI или контекста.")
    except Exception as e:
        logger.error(f"Ошибка в обработчике текстового сообщения: {e}")
        await update.message.reply_text("Произошла ошибка при обработке вашего сообщения.")
