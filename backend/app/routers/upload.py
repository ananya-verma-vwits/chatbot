from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.file_utils import save_file, extract_text_from_pdf, extract_text_from_docx
from services.document_processor import DocumentProcessor

router = APIRouter()
document_processor = DocumentProcessor()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a file."""
    file_path = save_file(file)
    try:
        # Extract text based on file type
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and DOCX are allowed.")
        
        print(f"Extracted text from file '{file.filename}': {text[:200]}")  # Print first 200 characters
        
        # Process the extracted text using DocumentProcessor
        document_processor.process_documents([text])
        return {"message": f"File '{file.filename}' uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")