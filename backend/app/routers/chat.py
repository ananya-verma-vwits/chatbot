import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.document_processor import document_processor
from utils.generate_response import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

# document_store = []
# embeddings_store = None

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
os.makedirs(FILES_DIR, exist_ok=True)

@router.post("/")
async def chat(request: ChatRequest):
    """Endpoint to ask a question based on uploaded documents."""
    try:
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
