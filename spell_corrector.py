from difflib import get_close_matches

# Simple offline vocabulary (safe starter list)
VOCAB = [
    "hi", "hello", "hey",
    "what", "is", "my", "name", "college", "skills", "location",
    "python", "java", "c", "c++",
    "where", "do", "i", "live",
    "thanks", "thank", "you"
]

def correct_word(word):
    matches = get_close_matches(word, VOCAB, n=1, cutoff=0.75)
    return matches[0] if matches else word

def correct_sentence(text: str):
    words = text.split()
    corrected = [correct_word(w) for w in words]
    return " ".join(corrected)
