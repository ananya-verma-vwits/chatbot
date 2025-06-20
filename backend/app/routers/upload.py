import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.file_utils import process_pdf_to_markdown, save_file
from services.document_processor import DocumentProcessor

router = APIRouter()
document_processor = DocumentProcessor()

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")  # Save files inside app/files
os.makedirs(FILES_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a file."""
    try:
        # Save the uploaded PDF file
        file_path = save_file(file)

        # Generate Markdown content from the PDF
        markdown_content = process_pdf_to_markdown(file_path)

        # Save the Markdown file in the same folder as the PDF
        filename = file.filename or "uploaded_file"
        markdown_file_path = os.path.join(FILES_DIR, f"{os.path.splitext(filename)[0]}.md")
        with open(markdown_file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return {
            "message": f"File '{file.filename}' uploaded and processed successfully.",
            "pdf_file": file_path,
            "markdown_file": markdown_file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")