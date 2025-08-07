import os
import PyPDF2
from docx import Document
from striprtf.striprtf import rtf_to_text

def read_file_content(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return read_txt(path)
    elif ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    elif ext == ".rtf":
        return read_rtf(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(path):
    doc = Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def read_rtf(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return rtf_to_text(content)
