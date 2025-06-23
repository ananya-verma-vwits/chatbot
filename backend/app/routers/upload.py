import logging
import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.file_utils import process_pdf_to_markdown, save_file
from services.document_processor import document_processor

router = APIRouter()

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")  # Save files inside app/files
os.makedirs(FILES_DIR, exist_ok=True)


@router.post("/")
async def upload_files(file: List[UploadFile] = File(...)):
    """Endpoint to upload a file."""
    try:
        results = []
        # Save the uploaded PDF file
        file_paths = [save_file(f) for f in file]

        # Process the document using the DocumentProcessor (FAISS)
        for f, file_path in zip(file, file_paths):
            document_processor.process_document(file_path)
            logging.info(f"Processed file: {file_path}")
            markdown_content = process_pdf_to_markdown(file_path)

        # Save the Markdown file in the same folder as the PDF
            filename = f.filename or "uploaded_file"
            markdown_file_path = os.path.join(FILES_DIR, f"{os.path.splitext(filename)[0]}.md")
            with open(markdown_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
        
            # json_path = os.path.join(FILES_DIR, f"{os.path.splitext(filename)[0]}.json")
            # pdf_to_structured_json(file_path, output_path=json_path)

            results.append({
                "filename": f.filename,
                "pdf_file": file_path,
                "markdown_file": markdown_file_path,
            })

        return {"message": f"Processed {len(results)} files successfully", "files": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    
@router.get("/status")
async def upload_status():
    """Return the list of uploaded PDF files."""
    try:
        # Get all PDF files in the FILES_DIR
        pdf_files = [f for f in os.listdir(FILES_DIR) if f.endswith(".pdf")]
        return {"files": pdf_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file status: {str(e)}")

@router.delete("/{filename}")
async def delete_file(filename: str):
    """Delete a file and rebuild the FAISS index."""
    try:
        # Create the full file path
        file_path = os.path.join(FILES_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File {filename} not found")
            
        # Delete the file
        os.remove(file_path)
        
        # Also delete any associated files (markdown, json)
        base_name = os.path.splitext(filename)[0]
        for ext in [".md", ".json"]:
            associated_file = os.path.join(FILES_DIR, f"{base_name}{ext}")
            if os.path.exists(associated_file):
                os.remove(associated_file)
        
        # Rebuild the FAISS index
        document_processor.vector_store = None  # Reset the vector store
        pdf_files = [f for f in os.listdir(FILES_DIR) if f.endswith(".pdf")]
        for pdf_file in pdf_files:
            file_path = os.path.join(FILES_DIR, pdf_file)
            document_processor.process_document(file_path)
        
        print(f"File {filename} deleted and FAISS index rebuilt successfully")
        
        return {"message": f"File {filename} deleted successfully and FAISS index rebuilt"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")