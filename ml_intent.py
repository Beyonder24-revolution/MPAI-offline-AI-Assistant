from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------------------
# TRAINING DATA (You can grow this later)
# ---------------------------
TRAIN_DATA = {
    "greet": [
        "hi", "hello", "hey", "hey there", "good morning",
        "good evening", "helo", "hii", "yo"
    ],
    "thanks": [
        "thanks", "thank you", "thx", "thanks a lot", "appreciate it"
    ],
    "mode": [
        "mode friendly", "mode mentor", "mode strict",
        "change mode", "switch mode"
    ],
    "normal": [
        "what is ai", "tell me something", "explain ml",
        "how are you", "what can you do"
    ]
}

# ---------------------------
# PREPARE DATA
# ---------------------------
sentences = []
labels = []

for intent, texts in TRAIN_DATA.items():
    for t in texts:
        sentences.append(t)
        labels.append(intent)

# ---------------------------
# VECTOR + MODEL
# ---------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sentences)

model = LogisticRegression()
model.fit(X, labels)

# ---------------------------
# PREDICT FUNCTION
# ---------------------------
def predict_intent(text: str) -> str:
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

def predict_intent(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["hi", "hello", "hey"]):
        return "greet"

    if any(w in text for w in ["thanks", "thank you"]):
        return "thanks"

    if text.startswith("mode "):
        return "mode"

    return "normal"

