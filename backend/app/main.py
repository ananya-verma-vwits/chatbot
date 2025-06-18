import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers.chat import router as chat_router  # Import the router
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from your_embedding_module import nlp, document_store, embeddings_store  # Adjust the import based on your project structure
from pydantic import BaseModel
from routers.chat import load_documents
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Did not find OPENAI_API_KEY. Please set it in the environment or .env file.")

class ChatRequest(BaseModel):
    query: str

app = FastAPI(title="RAG Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the router
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="The 'query' field is required.")
    try:
        print(f"Incoming request: {request.query}")  # Debugging log

        # Ensure document_store and embeddings_store are initialized
        if not document_store or embeddings_store is None:
            raise HTTPException(status_code=500, detail="Document store or embeddings are not initialized.")

        # Create embedding for the query using spaCy
        query_embedding = nlp(request.query).vector.reshape(1, -1)

        # Calculate similarities
        similarities = cosine_similarity(query_embedding, embeddings_store)[0]

        # Get top 3 most relevant documents
        top_indices = np.argsort(similarities)[-3:][::-1]
        context = "\n".join([document_store[i] for i in top_indices])

        # Get response from Ollama
        from ollama_config import generate_response
        response = generate_response(request.query, context=context)

        return {"response": response, "context": context}
    except Exception as e:
        print(f"Error processing chat request: {str(e)}")  # Debugging log
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.on_event("startup")
async def startup_event():
    try:
        load_documents()
        print("Documents loaded successfully.")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
    print("Application is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)

