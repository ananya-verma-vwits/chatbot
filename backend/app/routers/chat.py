from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.document_processor import DocumentProcessor
import os

router = APIRouter()
doc_processor = DocumentProcessor()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = f"docs/{file.filename}"
    os.makedirs("docs", exist_ok=True)  # Ensure the directory exists
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    try:
        doc_processor.process_document(file_path)
        return {"message": "File processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")