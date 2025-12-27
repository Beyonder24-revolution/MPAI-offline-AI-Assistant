import os
from PIL import Image
import pytesseract
from core.memory import save_memory

def read_image(file_path: str, allow_save=True):
    """Extract text from image, save in memory, and return text"""
    if not os.path.exists(file_path):
        print(f"[ImageReader] File not found: {file_path}")
        return ""

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

        if text.strip():
            key = f"{os.path.basename(file_path)}_ocr"
            save_memory(key, text, allow_save=allow_save)
            print(f"[ImageReader] Text extracted and saved as memory")
        else:
            print("[ImageReader] No text found in image")
        return text
    except Exception as e:
        print(f"[ImageReader] Error reading image: {e}")
        return ""
