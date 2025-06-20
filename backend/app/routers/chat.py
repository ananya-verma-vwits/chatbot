import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.embedding_service import process_documents
from utils.generate_response import generate_response
import numpy as np
import spacy

router = APIRouter()
nlp = spacy.load("en_core_web_md")

class ChatRequest(BaseModel):
    query: str

document_store = []
embeddings_store = None

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
os.makedirs(FILES_DIR, exist_ok=True)

@router.post("/")
async def chat(request: ChatRequest):
    """Endpoint to ask a question based on uploaded documents."""
    global document_store, embeddings_store
    if not document_store or embeddings_store is None:
        print("Document store or embeddings store is empty. Processing documents...")
        document_store, embeddings_store = process_documents(FILES_DIR)

    try:
        query_embedding = np.array(nlp(request.query).vector).reshape(1, -1)

        similarities = np.dot(embeddings_store, query_embedding.T).flatten()

        top_indices = np.argsort(similarities)[-3:][::-1]

        # Generate Markdown content for the top documents
        markdown_content = "# Relevant Documents\n\n"
        for i in top_indices:
            markdown_content += f"## Document {i + 1}\n\n"
            markdown_content += document_store[i] + "\n\n"

        print(f"Markdown Content passed to Ollama: {markdown_content[:200]}")  # Debugging log

        response = generate_response(query=request.query, markdown_content=markdown_content)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
