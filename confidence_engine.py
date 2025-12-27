import random

def confidence_reply(question: str):
    question = question.lower()

    if len(question.split()) <= 2:
        return random.choice([
            "Can you please explain a bit more?",
            "Do you want a simple or detailed answer?",
            "What exactly would you like to know?"
        ])

    if question.endswith("?"):
        return random.choice([
            "Let me think… can you clarify this?",
            "Are you asking for an explanation or an example?",
            "Can you rephrase it slightly?"
        ])

    return None
