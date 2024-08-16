from logger import logger1, logger2
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from dotenv import load_dotenv
import os
from file_handler import *


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Глобальная переменная для хранения контекста
context_memory = []

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    logger1.info("Команда /start получена")
    await update.message.reply_text('Приветик! Отправьте мне вопрос, и я постараюсь найти ответ.')

def get_name(*args):
    name = ' '.join(args)
    return name.upper()

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    logger1.info("От %s  получено сообщение:  ---  %s  ", get_name(update.message.chat.username, update.message.chat.first_name, update.message.chat.last_name), update.message.text)
    logger2.debug("что в объекте"+str(update))
    user_message = update.message.text
    response = get_response(user_message)
    await update.message.reply_text(response)

# Функция для получения ответа от ChatGPT с использованием контекста
def get_chatgpt_response_with_context(question: str) -> str:
    global context_memory
    context_memory.append({"role": "user", "content": question})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context_memory,
            max_tokens=150
        )
        answer = response['choices'][0]['message']['content'].strip()
        context_memory.append({"role": "assistant", "content": answer})
        return answer
    
    except openai.error.OpenAIError as e:
        logger1.error(f"OpenAI API error: {e}")
        return "Извините, произошла ошибка при обращении к OpenAI API."

# Функция для получения ответа
def get_response(question: str) -> str:
    
    # Сначала ищем ответ в файле
    response = search_in_file(question)
    if response:
        logger2.info("Такой ответ я выдал: %s", response)
        logger2.debug("контекст"+str(context_memory))
        return response

    # Если не найдено, обращаемся к ChatGPT с контекстом
    response = get_chatgpt_response_with_context(question)
    logger1.info("Такой ответ я выда из гпт: %s", response)
    logger1.debug("контекст"+str(context_memory))
    answ = f'мне надо походу в дебри лезть'
    return response