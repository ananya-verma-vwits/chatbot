from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.document_processor import DocumentProcessor
import os
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from spacy import load
# from .config import nlp, document_store, embeddings_store
#from your_embedding_module import process_documents


class ChatRequest(BaseModel):
    query: str

router = APIRouter()
doc_processor = DocumentProcessor()

logging.basicConfig(level=logging.INFO)

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

# @router.post("/chat")
# async def chat(request: ChatRequest):
#     if not request.query or not request.query.strip():
#         raise HTTPException(status_code=400, detail="The 'query' field is required and cannot be empty.")
    
#     try:
#         logging.info(f"Incoming request: {request.query}")
        
#         if not document_store or embeddings_store is None:
#             raise HTTPException(status_code=500, detail="Document store or embeddings are not initialized.")
        
#         # Create embedding for the query using spaCy
#         try:
#             query_embedding = nlp(request.query).vector.reshape(1, -1)
#         except Exception as e:
#             logging.error(f"Error creating query embedding: {str(e)}")
#             raise HTTPException(status_code=500, detail="Error creating query embedding.")
#         logging.info(f"Query embedding shape: {query_embedding.shape}")
        
#         # Calculate similarities
#         similarities = cosine_similarity(query_embedding, embeddings_store)[0]
#         logging.info(f"Similarities calculated: {similarities}")
        
#         # Get top 3 most relevant documents
#         top_indices = np.argsort(similarities)[-3:][::-1]
#         context = "\n".join([document_store[i] for i in top_indices])
#         logging.info(f"Context generated: {context[:500]}")  # Log first 500 characters
        
#         # Get response from Ollama
#         from ollama_config import generate_response
#         response = generate_response(request.query, context=context)
#         logging.info(f"Response generated: {response}")
        
#         return {"response": response, "context": context}
#     except Exception as e:
#         logging.error(f"Error processing chat request: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")



# FILES_DIR = "backend\file"  # Define the directory containing the documents

nlp = load("en_core_web_md")  # Load spaCy model

document_store = []
embeddings_store = []

def load_documents():
    files_dir = "C:\FastApi\chatbot\backend\file"  # Directory where files are uploaded
    global document_store, embeddings_store

    # Ensure the directory exists
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
        
    try:
        document_store = []
        embeddings_store = []

        # Iterate through all files in the directory
        for file_name in os.listdir(files_dir):
            file_path = os.path.join(files_dir, file_name)
            if file_name.endswith(".txt"):  # Example for text files
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    document_store.append(text)
                    embeddings_store.append(nlp(text).vector)

        # Convert embeddings to a NumPy array
        embeddings_store = np.array(embeddings_store)

        print(f"Loaded {len(document_store)} documents.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading documents: {str(e)}")