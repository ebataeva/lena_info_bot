from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from handlers.logger import Logger

logger = Logger('QuestionAnswerBaseLogger').get_logger()

class QuestionAnswerBase:
    def __init__(self, file_path='data.txt'):
        self.file_path = file_path
        self.questions_answers = []
        self.vectorizer = TfidfVectorizer()  # Создаем объект для векторизации текста
        self.model = None
        self.load_data()  # Загружаем вопросы и ответы из файла

    def load_data(self):
        """Загружает вопросы и ответы из файла и подготавливает модель поиска."""
        try:
            logger.info(f"Загрузка вопросов и ответов из файла '{self.file_path}'")
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            current_question = None
            current_answer = None

            for line in lines:
                if line.startswith("Вопрос:"):
                    current_question = line.replace("Вопрос:", "").strip()
                elif line.startswith("Ответ:") and current_question:
                    current_answer = line.replace("Ответ:", "").strip()
                    self.questions_answers.append((current_question, current_answer))
                    current_question = None

            # Создаем векторное представление вопросов
            questions = [q for q, _ in self.questions_answers]
            X = self.vectorizer.fit_transform(questions)

            # Обучаем модель для поиска ближайших соседей
            self.model = NearestNeighbors(n_neighbors=1, metric='cosine').fit(X)
            logger.info("Модель поиска ближайших соседей успешно создана.")
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")

    def search_approximate_answer(self, question):
        """Ищет наиболее похожий вопрос и возвращает связанный с ним ответ."""
        try:
            logger.info(f"Поиск ответа для вопроса: {question}")
            question_vec = self.vectorizer.transform([question])
            
            # Находим ближайшего соседа
            distances, indices = self.model.kneighbors(question_vec)
            best_match_index = indices[0][0]
            best_score = 1 - distances[0][0]  # Преобразуем косинусное расстояние в схожесть

            # Устанавливаем порог схожести
            if best_score >= 0.5:
                best_match_answer = self.questions_answers[best_match_index][1]
                logger.info(f"Найден ответ с похожестью {best_score:.2f}: {best_match_answer}")
                return best_match_answer
            else:
                logger.info("Похожий вопрос не найден.")
                return None
        except Exception as e:
            logger.error(f"Ошибка при поиске ответа: {e}")
            return None
