import os
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import docx

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")  # Save files inside app/files
os.makedirs(FILES_DIR, exist_ok=True)

def save_file(file: UploadFile) -> str:
    """Save an uploaded file to the server."""
    file_path = os.path.join(FILES_DIR, str(file.filename))
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading DOCX: {str(e)}")