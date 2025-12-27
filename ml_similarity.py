from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.questions = []
        self.answers = []
        self.matrix = None

    # ---------------------------
    # TRAIN MODEL
    # ---------------------------
    def train(self, qa_pairs):
        """
        qa_pairs = [(question, answer), ...]
        """
        if not qa_pairs:
            return

        self.questions = [q for q, a in qa_pairs]
        self.answers = [a for q, a in qa_pairs]

        self.matrix = self.vectorizer.fit_transform(self.questions)

    # ---------------------------
    # PREDICT WITH CONFIDENCE
    # ---------------------------
    def predict(self, query):
        if not self.matrix or not self.questions:
            return None

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]

        best_index = scores.argmax()
        confidence = float(scores[best_index])

        if confidence <= 0:
            return None

        best_answer = self.answers[best_index]
        return best_answer, confidence
