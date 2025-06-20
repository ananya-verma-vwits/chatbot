import os
from fastapi import APIRouter, HTTPException
from services.embedding_service import process_documents
from services.ollama_service import generate_response
import numpy as np
import spacy

router = APIRouter()
nlp = spacy.load("en_core_web_md")

# Initialize global stores for documents and embeddings
document_store = []
embeddings_store = None

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")  # Save files inside app/files
os.makedirs(FILES_DIR, exist_ok=True)

@router.post("/")
async def ask_question(question: str):
    """Endpoint to ask a question based on uploaded documents."""
    # Ensure document_store and embeddings_store are populated
    global document_store, embeddings_store
    if not document_store or embeddings_store is None:
        print("Document store or embeddings store is empty. Processing documents...")
        document_store, embeddings_store = process_documents(FILES_DIR)  # Populate document_store and embeddings_store

    try:
        # Create embedding for the query using spaCy
        query_embedding = nlp(question).vector.reshape(1, -1)
        
        # Calculate similarities
        similarities = np.dot(embeddings_store, query_embedding.T).flatten()
        
        # Get top 3 most relevant documents
        top_indices = np.argsort(similarities)[-3:][::-1]
        context = "\n".join([document_store[i] for i in top_indices])

        # Debugging log
        print(f"Context passed to Ollama: {context[:200]}")  # Print first 200 characters
        
        # Get response from Ollama
        response = generate_response(query=question, context=context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))