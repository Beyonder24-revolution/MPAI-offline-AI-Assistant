import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_online(query: str, context=None) -> str:
    if not query:
        return None

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ GROQ ERROR:", e)
        return None
