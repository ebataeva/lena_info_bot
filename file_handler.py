
# Функция для загрузки контекста из файла
def load_context_from_file():
    global context_memory
    context_memory = []
    with open('data.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.startswith("Вопрос:"):
            context_memory.append({"role": "user", "content": line.replace("Вопрос:", "").strip()})
        elif line.startswith("Ответ:"):
            context_memory.append({"role": "assistant", "content": line.replace("Ответ:", "").strip()})

# Функция для поиска ответа в текстовом файле
def search_in_file(question: str) -> str:
    with open('data.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    response = None
    found_question = False
    for line in lines:
        if line.startswith("Вопрос:") and question.lower() in line.lower():
            found_question = True
            continue
        if found_question and line.startswith("Ответ:"):
            response = line.replace("Ответ:", "").strip()
            break
    return response