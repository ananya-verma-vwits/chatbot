from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.embedding_service import document_store, embeddings_store
from services.ollama_service import generate_response
from sklearn.metrics.pairwise import cosine_similarity
import spacy

router = APIRouter()
nlp = spacy.load("en_core_web_md")

class ChatRequest(BaseModel):
    query: str

@router.post("/")
async def chat(request: ChatRequest):
    """Endpoint to chat with the bot."""
    if not request.query:
        raise HTTPException(status_code=400, detail="The 'query' field is required.")
    try:
        if not document_store or embeddings_store is None:
            raise HTTPException(status_code=400, detail="No documents loaded")
        
        # Create embedding for the query using spaCy
        query_embedding = nlp(request.query).vector.reshape(1, -1)
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, embeddings_store)[0]
        
        # Get top 3 most relevant documents
        top_indices = np.argsort(similarities)[-3:][::-1]
        context = "\n".join([document_store[i] for i in top_indices])
        
        # Get response from Ollama
        response = generate_response(request.query, context=context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))