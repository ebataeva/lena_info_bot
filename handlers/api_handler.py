import openai
from handlers.logger import Logger

logger = Logger('APIHandlerLogger').get_logger()

# Предварительная обработка вопроса для добавления контекста
def preprocess_prompt(prompt: str) -> str:
    # Если ключевых слов нет, добавим общий контекст
    return f"{prompt}. Ответьте в контексте блокчейна и криптовалют."

def get_openai_response(context_memory):
    try:
        # Более конкретное системное сообщение
        system_message = {
            "role": "system",
            "content": (
                "You are an expert in blockchain and cryptocurrencies. "
                "Interpret all questions within the context of blockchain, cryptocurrencies, and related technologies. "
                "When the user mentions terms like 'wallet', assume they are referring to a cryptocurrency wallet, "
                "not a physical wallet."
            )
        }
        
        # Проверяем, что каждый элемент в контексте имеет правильный формат
        messages = [system_message]  # Начинаем с системного сообщения
        for entry in context_memory:
            if isinstance(entry, dict) and "role" in entry and "content" in entry:
                messages.append({"role": entry["role"], "content": str(entry["content"])})
            else:
                logger.warning(f"Пропущен некорректный элемент контекста: {entry}")

        # Запрос к OpenAI с учетом контекста
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=600,  # Увеличиваем количество токенов для более длинных ответов
            temperature=0.7,  # Контролируем креативность и разнообразие ответов
            top_p=0.9  # Используем вероятностное отсечение слов для генерации более естественных ответов
        )
        
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return None
