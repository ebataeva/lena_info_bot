from handlers.file_handler import load_text_from_word
from handlers.api_handler import send_to_openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os
from handlers.logger import Logger

logger = Logger('QuestionAnswerBaseLogger').get_logger()

class QuestionAnswerBase:
    def __init__(self, openai_api_key, word_file_path='documentation.docx'):
        self.word_file_path = word_file_path
        self.documentation_text = ""
        self.documentation_paragraphs = []
        self.vectorizer = TfidfVectorizer()
        self.documentation_model = None
        self.load_data()  # Загружаем данные из Word-документа
        self.prompt = (
            lambda intro, documentation_text, question, question_prompt : 
            (
                f'{intro}:\n'
                f'{documentation_text}\n\n'
                f'Вопрос: {question}\n'
                f'{question_prompt}'
            )
        )
        self.map = {    
            'intro': 'Вот текст из документации:',
            'question_prompt': (
                'Умоляю, дайте наилучший ответ, '
                'основанный на этом тексте.',
            )
        }

    def load_data(self):
        # Загружает текст из Word-документа и подготавливает модель поиска.
        try:
            # Загружаем текст из Word-документа
            if os.path.exists(self.word_file_path):
                self.documentation_text = (
                    load_text_from_word(self.word_file_path)
                )
                self.documentation_paragraphs = (
                    self.documentation_text.split('\n')  # Разбиваем текст на абзацы
                )
                logger.info(f'Текст из Word-документа загружен: '
                            '{len(self.documentation_paragraphs)} абзацев')

                # Создаем векторное представление абзацев и обучаем модель
                if self.documentation_paragraphs:
                    doc_vectors = self.vectorizer.fit_transform(
                        self.documentation_paragraphs
                        )
                    self.documentation_model = NearestNeighbors(
                        n_neighbors=1, 
                        metric='cosine'
                    ).fit(doc_vectors)
                    logger.info('Модель поиска по документации создана.')
            else:
                logger.warning(f'Файл "{self.word_file_path}" не найден.')
        except Exception as e:
            logger.error(f'Ошибка при загрузке данных: {e}')

    def search_in_word_document(self, question):
        # Ищет наиболее похожий абзац в документации
        try:
            if not self.documentation_paragraphs:
                logger.warning('Документация отсутствует или пуста.')
                return None

            # Векторизуем вопрос
            question_vector = self.vectorizer.transform([question])

            # Поиск в документации
            distances, indices = self.documentation_model.kneighbors(
                question_vector
            )
            closest_paragraph = self.documentation_paragraphs[indices[0][0]]
            logger.info(f'Сравнение с абзацем: "{closest_paragraph}", '
                        f'схожесть: {1 - distances[0][0]}')

            # Устанавливаем порог схожести (например, 0.5)
            if distances[0][0] < 0.5:
                if len(closest_paragraph) < 50:
                    logger.info('Ответ слишком короткий, обращаемся к OpenAI.')
                    return self.query_openai(question)
                return closest_paragraph

            # Если не нашли похожий абзац, используем OpenAI
            logger.info('Похожий абзац не найден, обращаемся к OpenAI.')
            return self.query_openai(question)
        except Exception as e:
            logger.error(f'Ошибка при поиске в документации: {e}')
            return None

    def query_openai(self, question):
        # Запрашивает OpenAI с учетом документации
        try:
            prompt = self.prompt(
                self.map['intro'], 
                self.documentation_text, 
                question,
                self.map['question_prompt'])
            return send_to_openai(prompt)
        except Exception as e:
            logger.error(f'Ошибка при запросе к OpenAI: {e}')
            return None
