import re

INTENTS = {
    "greeting": [
        "hi", "hello", "hey", "hii", "hey bro", "good morning", "good evening"
    ],
    "farewell": [
        "bye", "goodbye", "see you", "take care"
    ],
    "thanks": [
        "thanks", "thank you", "thx"
    ]
}

def normalize(text: str):
    text = text.lower().strip()

    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    for intent, phrases in INTENTS.items():
        if text in phrases:
            return intent

    return text
def detect_intent(text: str):
    t = text.lower()

    if any(w in t for w in ["hi", "hello", "hey"]):
        return "greet"

    if "my name is" in t:
        return "teach_name"

    if any(w in t for w in ["what is", "who is", "tell me about"]):
        return "question"

    if any(w in t for w in ["do you know", "are you aware"]):
        return "yes_no_question"

    if any(w in t for w in ["learn", "remember", "save this"]):
        return "teach_fact"

    return "unknown"
def wants_online(text: str) -> bool:
    online_keywords = [
        "search", "online", "latest", "current",
        "news", "today", "now", "internet", "google"
    ]
    return any(word in text for word in online_keywords)

