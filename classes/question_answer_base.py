from handlers.file_handler import load_text_from_word
from handlers.api_handler import send_to_openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os
from handlers.logger import Logger
import openai

logger = Logger('QuestionAnswerBaseLogger').get_logger()

class QuestionAnswerBase:
    def __init__(self, openai_api_key, word_file_path='documentation.docx'):
        self.word_file_path = word_file_path
        self.documentation_text = ""
        self.documentation_paragraphs = []
        self.vectorizer = TfidfVectorizer()
        self.documentation_model = None
        openai.api_key = openai_api_key
        self.load_data()  # Загружаем данные из Word-документа

    def load_data(self):
        """Загружает текст из Word-документа и подготавливает модель поиска."""
        try:
            # Загружаем текст из Word-документа
            if os.path.exists(self.word_file_path):
                self.documentation_text = load_text_from_word(self.word_file_path)
                self.documentation_paragraphs = self.documentation_text.split('\n')  # Разбиваем текст на абзацы
                logger.info(f"Текст из Word-документа загружен: {len(self.documentation_paragraphs)} абзацев")

                # Создаем векторное представление абзацев и обучаем модель
                if self.documentation_paragraphs:
                    doc_vectors = self.vectorizer.fit_transform(self.documentation_paragraphs)
                    self.documentation_model = NearestNeighbors(n_neighbors=1, metric='cosine').fit(doc_vectors)
                    logger.info("Модель поиска по документации успешно создана.")
            else:
                logger.warning(f"Файл '{self.word_file_path}' не найден.")
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")

    def search_in_word_document(self, question):
        """Ищет наиболее похожий абзац в документации."""
        try:
            if not self.documentation_paragraphs:
                logger.warning("Документация отсутствует или пуста.")
                return None

            # Векторизуем вопрос
            question_vector = self.vectorizer.transform([question])

            # Поиск в документации
            distances, indices = self.documentation_model.kneighbors(question_vector)
            closest_paragraph = self.documentation_paragraphs[indices[0][0]]
            logger.info(f"Сравнение с абзацем: '{closest_paragraph}', схожесть: {1 - distances[0][0]}")

            # Устанавливаем порог схожести (например, 0.5)
            if distances[0][0] < 0.5:
                return closest_paragraph

            # Если не нашли похожий абзац, используем OpenAI
            logger.info("Похожий абзац не найден, обращаемся к OpenAI.")
            return self.query_openai(question)
        except Exception as e:
            logger.error(f"Ошибка при поиске в документации: {e}")
            return None

    def query_openai(self, question):
        """Запрашивает OpenAI с учетом документации."""
        try:
            prompt = f"Вот текст из документации:\n{self.documentation_text}\n\nВопрос: {question}\nПожалуйста, дайте наилучший ответ, основанный на этом тексте."
            return send_to_openai(prompt)
        except Exception as e:
            logger.error(f"Ошибка при запросе к OpenAI: {e}")
            return None
