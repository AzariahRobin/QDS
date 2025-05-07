import pdfplumber
import docx
import pytesseract
from PIL import Image
import os

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return extract_pdf_text(filepath)
    elif ext == '.docx':
        return extract_docx_text(filepath)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return extract_image_text(filepath)
    else:
        return "Unsupported file format."

def extract_pdf_text(path):
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text.strip()

def extract_docx_text(path):
    doc = docx.Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_image_text(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image)