import os
from pypdf import PdfReader
from core.memory import save_memory

def read_pdf(file_path: str, allow_save=True):
    """Extract text from PDF and save each page as memory"""
    if not os.path.exists(file_path):
        print(f"[DocumentReader] File not found: {file_path}")
        return

    reader = PdfReader(file_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            key = f"{os.path.basename(file_path)}_page_{i+1}"
            save_memory(key, text, allow_save=allow_save)
            print(f"[DocumentReader] Page {i+1} saved as memory")
from core.memory import save_memory, search_memory

def store_pdf_text(pdf_name, page_num, text):
    """Save each page text as separate memory key"""
    key = f"{pdf_name}_page_{page_num}"
    save_memory(key, text)

def ask_pdf_question(pdf_name, question):
    """Search PDF pages for answer"""
    matches = search_memory(pdf_name)
    if not matches:
        return "I have no info about this document."

    question_lower = question.lower()
    for _, key, value, _ in matches:
        if question_lower in value.lower():
            return f"Found in {key}: {value[:200]}..."  # first 200 chars

    return "Sorry, I couldn't find the answer in this document."
