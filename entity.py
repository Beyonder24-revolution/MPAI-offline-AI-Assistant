def extract_entity(text: str):
    t = text.lower()

    keywords = [
        "python", "dog", "cat", "ai", "machine learning",
        "name", "language", "animal"
    ]

    for k in keywords:
        if k in t:
            return k

    return None
