import openai
from logger import Logger

logger = Logger('APIHandlerLogger').get_logger()

# Предварительная обработка вопроса для добавления контекста
def preprocess_prompt(prompt: str) -> str:
    # Ключевые слова для добавления контекста
    keywords = ["кошелек", "безопасность", "торговля", "валюта", "криптовалюта", "блокчейн", "биткоин", "ethereum"]
    
    # Если в вопросе пользователя есть одно из ключевых слов, добавим контекст
    if any(keyword in prompt.lower() for keyword in keywords):
        return f"{prompt} в контексте криптовалюты и блокчейна."
    
    # Если ключевых слов нет, добавим общий контекст
    return f"{prompt}. Ответьте в контексте блокчейна и криптовалют."

# Функция для отправки запроса к OpenAI API
import openai
from logger import Logger

logger = Logger('APIHandlerLogger').get_logger()

def get_openai_response(context_memory):
    try:
        # Проверяем, что каждый элемент в контексте имеет правильный формат
        messages = []
        for entry in context_memory:
            if isinstance(entry, dict) and "role" in entry and "content" in entry:
                # Добавляем только корректные элементы
                messages.append({"role": entry["role"], "content": str(entry["content"])})
            else:
                logger.warning(f"Пропущен некорректный элемент контекста: {entry}")

        # Отправляем запрос в OpenAI с учетом контекста
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )
        
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return None
