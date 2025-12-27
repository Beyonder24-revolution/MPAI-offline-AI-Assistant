# core/personality.py

import random

PERSONALITIES = {
    "friendly": {
        "greet": [
            "Hey 👋 How can I help you?",
            "Hi there! What can I do for you?",
            "Hello 😊 How may I assist you today?"
        ],
        "unknown": [
            "Hmm 🤔 I don’t know that yet. Can you teach me?",
            "I’m not fully sure about that — can you explain it to me?",
            "That’s new for me 🙂 Want to teach me?"
        ],
        "confirm": [
            "Got it! I’ll remember that 😊",
            "Saved 👍 Thanks for teaching me!",
            "Alright! I’ve learned this."
        ],
        "thanks": [
            "You're welcome 😄",
            "Anytime!",
            "Happy to help 😊"
        ],
        "fallback": [
            "Can you tell me a bit more?",
            "I didn’t fully get that — could you rephrase?",
            "Let’s try that again 🙂"
        ]
    },

    "mentor": {
        "greet": [
            "Hello. How can I assist you today?",
            "Hi. What would you like to work on?",
            "Welcome. Ask me anything."
        ],
        "unknown": [
            "I don’t have that information yet. Please teach me.",
            "That’s outside my current knowledge. You can help me learn.",
            "I’m unsure about this. Let’s figure it out together."
        ],
        "confirm": [
            "Noted. I’ve saved this information.",
            "Understood. This has been recorded.",
            "Good. I’ll remember this going forward."
        ],
        "thanks": [
            "Glad to help.",
            "You’re welcome.",
            "Always happy to assist."
        ],
        "fallback": [
            "Could you clarify your question?",
            "Let’s rephrase that for better understanding.",
            "Please provide a bit more context."
        ]
    },

    "strict": {
        "greet": ["Speak."],
        "unknown": ["Unknown. Teach me."],
        "confirm": ["Saved."],
        "thanks": ["Okay."],
        "fallback": ["Repeat clearly."]
    }
}

current_mode = "friendly"


# ---------------------------
# MODE CONTROL
# ---------------------------
def set_mode(mode: str):
    global current_mode
    if mode in PERSONALITIES:
        current_mode = mode
        return f"Personality switched to {mode}"
    return "Invalid personality mode"


# ---------------------------
# MAIN REPLY HANDLER
# ---------------------------
def reply(key: str):
    responses = PERSONALITIES.get(current_mode, {})
    value = responses.get(key)

    if isinstance(value, list):
        return random.choice(value)

    return value or random.choice(
        PERSONALITIES[current_mode].get("fallback", ["..."])
    )
