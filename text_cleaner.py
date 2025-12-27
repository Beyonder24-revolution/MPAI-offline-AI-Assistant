import re

def clean_text(text):
    return "".join(c.lower() for c in text if c.isalnum())


    text = text.lower().strip()

    # keep letters, numbers, spaces, basic punctuation
    text = re.sub(r"[^a-z0-9\s?.!']", "", text)

    # normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text
