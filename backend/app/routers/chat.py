import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.document_processor import document_processor
from services.embedding_service import process_documents
from utils.generate_response import generate_response
import numpy as np
import spacy

router = APIRouter()
nlp = spacy.load("en_core_web_md")

class ChatRequest(BaseModel):
    query: str

# document_store = []
# embeddings_store = None

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
os.makedirs(FILES_DIR, exist_ok=True)

@router.post("/")
async def chat(request: ChatRequest):
    """Endpoint to ask a question based on uploaded documents."""
    # global document_store, embeddings_store
    # if not document_store or embeddings_store is None:
    #     print("Document store or embeddings store is empty. Processing documents...")
    #     document_store, embeddings_store = process_documents(FILES_DIR)

        # Replace the current loop with this code
        # Process all PDF files in the directory directly
    # pdf_files = [f for f in os.listdir(FILES_DIR) if f.endswith(".pdf")]
    # for pdf_file in pdf_files:
    #     file_path = os.path.join(FILES_DIR, pdf_file)
    #     try:
    #         document_processor.process_document(file_path)
    #         print(f"Processed file: {pdf_file}")
    #     except Exception as e:
    #         print(f"Error processing file {pdf_file}: {str(e)}")


    try:
        # # Query documents using FAISS
        # if not document_store or embeddings_store is None:
        #     raise HTTPException(status_code=400, detail="No documents have been uploaded yet. Please upload documents first.")
        
        # Get relevant document chunks from FAISS
        top_chunks = document_processor.query_documents(request.query, k=3)

        if not top_chunks:
            return {"response": "No relevant information found in the uploaded documents."}
        
        # Combine the chunks into a single context
        markdown_content = "# Relevant Document Sections\n\n"
        for i, chunk in enumerate(top_chunks):
            markdown_content += f"## Section {i + 1}\n\n{chunk}\n\n"
        
        print(f"Markdown Content passed to Ollama: {markdown_content[:200]}")  # Debugging log
        
        # Generate response based on the retrieved content
        response = generate_response(query=request.query, markdown_content=markdown_content)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/status")
async def faiss_status():
    """Check the status of the FAISS vector store."""
    try:
        if document_processor.vector_store:
            try:
                # Get document count if possible
                doc_count = len(document_processor.vector_store.index_to_docstore_id)
                return {
                    "status": "initialized",
                    "document_count": doc_count
                }
            except Exception as e:
                return {
                    "status": "initialized",
                    "error_getting_count": str(e)
                }
        else:
            return {"status": "not_initialized"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

        
# @router.post("/")
# async def chat(request: ChatRequest):
#     """Endpoint to ask a question based on uploaded documents."""
#     try:
#         # Dynamically find the Markdown file based on the PDF file name
#         pdf_files = [f for f in os.listdir(FILES_DIR) if f.endswith(".pdf")]
#         if not pdf_files:
#             raise HTTPException(status_code=400, detail="No PDF file available for querying.")

#         # Assume the first PDF file is the one to use (you can enhance this logic as needed)
#         pdf_file_name = pdf_files[0]
#         markdown_file_name = f"{os.path.splitext(pdf_file_name)[0]}.md"
#         markdown_file_path = os.path.join(FILES_DIR, markdown_file_name)

#         if not os.path.isfile(markdown_file_path):
#             raise HTTPException(status_code=400, detail="No Markdown file available for querying.")

#         # Read Markdown content from the dynamically determined file
#         with open(markdown_file_path, "r", encoding="utf-8") as f:
#             markdown_content = f.read()

#         print(f"Markdown Content passed to Ollama: {markdown_content[:200]}")  # Debugging log

#         # Pass Markdown content directly to the LLM
#         response = generate_response(query=request.query, markdown_content=markdown_content)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))