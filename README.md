Here’s the translated version of the README:

---

# Telegram ChatBot with OpenAI and Context Support

This project is a Telegram bot integrated with the OpenAI API. It provides answers to questions based on documentation (Word documents) and the user's previous interactions. The bot uses machine learning to find the most relevant answers and can query OpenAI if the required information is not found in the local database.

## 📋 **Technologies and Libraries**

The project is built using the following technologies and libraries:
- `Python 3.8+`
- `python-telegram-bot` for interacting with the Telegram API
- `openai` for integration with OpenAI GPT-3.5
- `colorama` for colorful logging
- `scikit-learn` for text vectorization and nearest neighbors search
- `python-docx` for working with Word documents

## 📁 **Project Structure**

```

/project-root
│
├── bot.py                      # Main file to launch the bot
├── requirements.txt            # Project dependencies
│
├── classes/                    # Classes for handling various tasks
│   ├── bot_class.py            # ChatBot class for command and message handling
│   └── question_answer_base.py # Class for searching answers in documentation
│
├── handlers/                   # Handlers for commands and APIs
│   ├── handler.py              # Handlers for bot commands and messages
│   ├── api_handler.py          # Functions for interacting with the OpenAI API
│   ├── file_handler.py         # Functions for file handling (uploading, searching, context saving)
│   └── logger.py               # Logging setup with color customization
│
└── contexts/                   # Stores files with user context
    └── context_user_chat_id.txt # Context files for each user

```

## ⚙️ **Installation and Setup**
Assuming Python 3.8+, IDE (e.g., VSCode), pip, and git are already installed:

1. **Clone the repository:**
   ```bash
   git clone <git@github.com:ebataeva/lena_info_bot.git>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Add environment variables for your Telegram Bot Token and OpenAI API Key:
     ```
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## ▶️ **Running the Bot**

1. Launch the bot using the following command:
   ```bash
   python bot.py
   ```

2. The bot will start interacting with users on Telegram, processing commands and responding to messages.

## 🗃 **Project Files**

### 1. **bot.py**
   - The main file for launching the bot. It loads environment variables, initializes the `ChatBot` instance, and calls its `start()` method. Handles bot initialization and error management.

### 2. **bot_class.py**
   - The `ChatBot` class manages the bot's core functionality, including processing `/start` and `/clear` commands as well as text messages from users. It uses the `QuestionAnswerBase` class to search for answers in documentation.

### 3. **handler.py**
   - Contains handlers for commands and messages. Handles user context saving and loading, and interacts with OpenAI for generating answers.

### 4. **logger.py**
   - Configures colorful logging for different project components using `colorama`.

### 5. **file_handler.py**
   - Utility functions for file operations such as loading text from Word documents, saving/loading user context, and searching for answers in the local database.

### 6. **api_handler.py**
   - Responsible for interacting with the OpenAI API. Contains functions for sending requests to OpenAI and processing responses.

### 7. **question_answer_base.py**
   - The `QuestionAnswerBase` class handles answer searching within Word documentation. Uses a nearest neighbors method from `scikit-learn` to find the most relevant paragraphs.

### 8. **requirements.txt**
   - Lists all necessary libraries and dependencies used in the project.

## 🚀 **How to Use**

- After launching the bot, send the `/start` command in the Telegram chat to initialize the dialogue.
- Send the bot a question, and it will try to find an answer in the uploaded documentation or query OpenAI for additional information.

## 🛠 **Requirements**

- Python 3.8+
- Installed and configured `pip`
- Accounts and tokens for Telegram and OpenAI

## 📝 **Notes**
- The bot supports storing context from previous interactions for more personalized answers.
- Colorful logging is implemented for better traceability of bot performance and error handling.

## 🧑‍💻 **Author**
- https://github.com/ebataeva/

--- 

