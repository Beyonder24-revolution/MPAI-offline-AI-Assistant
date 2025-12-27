import os
import requests

API_KEY = os.getenv("ONLINE_API_KEY")

def fetch_online_knowledge(query: str) -> str | None:
    if not API_KEY:
        return None

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.7
            },
            timeout=15
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return None
