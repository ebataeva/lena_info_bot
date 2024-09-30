

# Telegram ChatBot с OpenAI и Поддержкой Контекста

Этот проект представляет собой Telegram-бота, 
который интегрируется с OpenAI API и предоставляет ответы на вопросы, основанные на документации (Word-документ) 
и предыдущих взаимодействиях пользователя. Бот использует механизм машинного обучения для нахождения наиболее релевантных ответов, 
а также может обращаться к OpenAI, если нужная информация не найдена в локальной базе данных.

## 📋 **Технологии и библиотеки**

Проект реализован с использованием следующих технологий и библиотек:
- `Python 3.8+`
- `python-telegram-bot` для взаимодействия с Telegram API
- `openai` для интеграции с OpenAI GPT-3.5
- `colorama` для цветного логирования
- `scikit-learn` для векторизации текста и поиска ближайших соседей
- `python-docx` для работы с Word-документами

## 📁 **Структура проекта**

```

/project-root
│
├── bot.py                      # Главный файл для запуска бота
├── requirements.txt            # Зависимости проекта
│
├── classes/                    # Классы для обработки различных задач
│   ├── bot_class.py            # Класс ChatBot для обработки команд и сообщений
│   └── question_answer_base.py # Класс для поиска ответов в документации
│
├── handlers/                   # Обработчики для команд и API
│   ├── handler.py              # Обработчики команд и сообщений для бота
│   ├── api_handler.py          # Функции для взаимодействия с OpenAI API
│   ├── file_handler.py         # Функции для работы с файлами (загрузка, поиск, сохранение контекста)
│   └── logger.py               # Настройка и кастомизация логирования с цветами
│
└── contexts/                   # Хранение файлов с пользовательским контекстом
    └── context_user_chat_id.txt # Файлы с контекстом для каждого пользователя

```

## ⚙️ **Установка и настройка**
С учетом, что уже установлены python3.8+, IDE (я использую VScode), pip, git

1. **Клонируйте репозиторий:**
   ```bash
   git clone <git@github.com:ebataeva/lena_info_bot.git>
   ```

2. **Создайте виртуальное окружение и активируйте его:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. **Установите необходимые зависимости:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Настройка переменных окружения:**
   - Создайте переменный окружения и передайте туда ваш Telegram Bot Token и OpenAI API Key:
     ```
     TELEGRAM_BOT_TOKEN=ваш_токен_бота
     OPENAI_API_KEY=ваш_openai_api_key
     ```

## ▶️ **Запуск бота**

1. Запустите бота, выполнив следующую команду:
   ```bash
   python bot.py
   ```

2. Бот начнет взаимодействовать с пользователями в Telegram, обрабатывая команды и отвечая на сообщения.

## 🗃 **Файлы проекта**

### 1. **bot.py**
   - Главный файл для запуска бота. Загружает переменные окружения, создает экземпляр `ChatBot` и запускает его метод `start()`. Отвечает за инициализацию бота и обработку ошибок.

### 2. **bot_class.py**
   - Класс `ChatBot` управляет основным функционалом бота, включая обработку команд `/start` и `/clear`, а также текстовых сообщений от пользователей. Использует класс `QuestionAnswerBase` для поиска ответов в документации.

### 3. **handler.py**
   - Содержит обработчики команд и сообщений. Загрузчик и сохранение контекста пользователей. Взаимодействует с OpenAI для получения ответов на вопросы.

### 4. **logger.py**
   - Настраивает цветное логирование для разных компонентов проекта. Использует `colorama` для настройки цветов и форматирования сообщений логов.

### 5. **file_handler.py**
   - Вспомогательные функции для работы с файлами, такие как загрузка текста из Word-документов, сохранение и загрузка контекста в файл, а также поиск ответов в локальной базе данных.

### 6. **api_handler.py**
   - Отвечает за взаимодействие с OpenAI API. Содержит функции для отправки запросов к OpenAI и обработки ответов.

### 7. **question_answer_base.py**
   - Класс `QuestionAnswerBase` отвечает за поиск ответов в Word-документации. Использует метод ближайших соседей из `scikit-learn` для нахождения наиболее релевантных абзацев.

### 8. **requirements.txt**
   - Содержит список всех необходимых библиотек и зависимостей, используемых в проекте.

## 🚀 **Как использовать**

- После запуска бота отправьте команду `/start` в чате Telegram, чтобы инициализировать диалог.
- Отправьте боту вопрос, и он попытается найти ответ в загруженной документации или обратиться к OpenAI для получения дополнительной информации.

## 🛠 **Требования**

- Python 3.8+
- Установленный и настроенный `pip`
- Учетные записи и токены для Telegram и OpenAI

## 📝 **Примечания**
- Бот поддерживает хранение контекста предыдущих взаимодействий для более персонализированных ответов.
- Реализовано цветное логирование для лучшей отслеживаемости работы бота и обработки ошибок.

## 🧑‍💻 **Автор**
- https://github.com/ebataeva/

