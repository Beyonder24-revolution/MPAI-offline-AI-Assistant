import random

SMART_FALLBACKS = [
    "I’m not fully sure yet, but you can teach me 😊",
    "I don’t have this in memory yet — want to teach me?",
    "I’m still learning this. You can help me improve.",
    "That’s new for me. Teach me once, I’ll remember forever."
]

CONFIRMATIONS = [
    "Got it 👍",
    "Alright, saved.",
    "Done. I’ll remember that.",
    "Noted."
]

def smart_fallback():
    return random.choice(SMART_FALLBACKS)

def confirm_save():
    return random.choice(CONFIRMATIONS)
