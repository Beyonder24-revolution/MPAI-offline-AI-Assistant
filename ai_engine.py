from core.online_ai import ask_online
from core.generic_knowledge import GENERIC_KNOWLEDGE
from core.personality import reply, set_mode
from core.text_cleaner import clean_text
from core.memory import save_memory, search_memory
from core.ml_similarity import SimilarityEngine
import random

PROFILE_KEYS = {
    "name": ["my name is", "call me"],
    "college": ["my college is", "i study at"],
    "skill": ["i know", "i am good at"],
    "location": ["i live in", "i am from"]
}


class OfflineAI:
    def __init__(self, context_size=5):
        self.context_size = context_size
        self.recent_context = []
        self.similarity = SimilarityEngine()

    # ===========================
    # MAIN ASK FUNCTION
    # ===========================
    def ask(self, question: str):
        q = clean_text(question)

        if not q:
            return "Please type something 🙂"

        # 1️⃣ PROFILE MEMORY
        profile_reply = self._detect_profile(q)
        if profile_reply:
            return profile_reply

        # 2️⃣ MODE / BASIC INTENTS
        if q.startswith("mode "):
            return set_mode(q.replace("mode", "").strip())

        if q in ["hi", "hello", "hey"]:
            return reply("greet")

        if q in ["thanks", "thank you"]:
            return reply("thanks")

        # 3️⃣ MEMORY EXACT MATCH
        exact = search_memory(q)
        if exact:
            answer = exact[0][2]
            self._update_context(q, answer)
            return self._human_reply(answer)

        # 4️⃣ GENERIC KNOWLEDGE
        for key, info in GENERIC_KNOWLEDGE.items():
            if key in q:
                return (
                    f"{info}\n\n"
                    "Would you like a deeper explanation or should I remember this?"
                )

        # 5️⃣ ML SIMILARITY (OPTIONAL)
        ml_result = self.similarity.predict(q)
        if ml_result:
            ml_answer, confidence = ml_result
            if confidence >= 0.65:
                self._update_context(q, ml_answer)
                return (
                    f"{self._human_reply(ml_answer)}\n\n"
                    f"🔍 Confidence: {round(confidence * 100)}%"
                )

        # 6️⃣ ONLINE (GROQ DEFAULT)
        online_reply = ask_online(q, self.recent_context)
        if online_reply:
            return online_reply

        # 7️⃣ FINAL SMART FALLBACK
        return (
            "🤔 I don’t have a clear answer yet.\n\n"
            "You can say:\n"
            "• explain\n"
            "• search online 🌐\n"
            "• or teach me\n"
        )

    # ===========================
    # PROFILE MEMORY
    # ===========================
    def _detect_profile(self, q):
        for key, patterns in PROFILE_KEYS.items():
            for p in patterns:
                if q.startswith(p):
                    value = q.replace(p, "").strip()
                    if value:
                        save_memory(f"user_{key}", value)
                        return f"Got it 😊 I’ll remember your {key}."

        if q in ["what is my name", "my name", "name"]:
            return self._recall("user_name", "your name")

        if q in ["where do i live", "my location"]:
            return self._recall("user_location", "where you live")

        return None

    def _recall(self, key, label):
        data = search_memory(key)
        if data:
            return f"As I remember, {label} is {data[0][2]}."
        return f"I don’t know {label} yet."

    # ===========================
    # HUMAN RESPONSE STYLE
    # ===========================
    def _human_reply(self, answer):
        answer = answer.strip().capitalize()
        if not answer.endswith("."):
            answer += "."
        return random.choice([
            answer,
            f"Sure 🙂 {answer}",
            f"As I remember, {answer}"
        ])

    # ===========================
    # CONTEXT
    # ===========================
    def _update_context(self, q, a):
        self.recent_context.append((q, a))
        if len(self.recent_context) > self.context_size:
            self.recent_context.pop(0)
