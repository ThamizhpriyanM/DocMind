import fitz
import os

def extract_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not pdf_path.endswith(".pdf"):
        raise ValueError(f"Expected a .pdf file, got: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    all_text = " "

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        all_text += text + "\n"

    doc.close()
    return all_text

def extract_text_with_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages.append({
            "page": page_num + 1,
            "text": text
        })
    
    doc.close()
    return pages

def clean_text(text):
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip()]
    return " ".join(cleaned)