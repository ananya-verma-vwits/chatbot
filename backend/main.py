from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader  # Updated import
import numpy as np
import os
import shutil
from PyPDF2 import PdfReader
import docx
import torch
torch.set_default_device("cpu")
print(f"Default device: {torch.device('cpu')}")
print(f"Is MPS available: {torch.backends.mps.is_available()}")
from transformers import pipeline



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize spaCy model and storage
nlp = spacy.load('en_core_web_md')
document_store = []
embeddings_store = None

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

# Directory to store pre-existing and uploaded files
FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)

# Load a question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", device=-1)

def process_documents(texts):
    global document_store, embeddings_store
    
    # Store the actual text chunks
    if not document_store:
        document_store = texts
    else:
        document_store.extend(texts)
    
    # Create embeddings using spaCy
    new_embeddings = np.array([nlp(text).vector for text in texts])
    
    if embeddings_store is None:
        embeddings_store = new_embeddings
    else:
        embeddings_store = np.vstack([embeddings_store, new_embeddings])

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        print(f"Extracted text from PDF: {text}")  # Debugging log
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        print(f"Extracted text from DOCX: {text}")  # Debugging log
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading DOCX: {str(e)}")

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="The 'query' field is required.")
    try:
        print(f"Incoming request: {request}")  # Debugging log
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
        from ollama_config import generate_response
        response = generate_response(request.query, context=context)
        
        return {"response": response, "context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a file."""
    file_path = os.path.join(FILES_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/files")
async def list_files():
    """Endpoint to list all files."""
    files = os.listdir(FILES_DIR)
    return {"files": files}

@app.get("/answer")
async def answer_question(question: str):
    """Endpoint to answer a question using the ingested files."""
    files = os.listdir(FILES_DIR)
    if not files:
        raise HTTPException(status_code=404, detail="No files available for processing.")
    
    combined_text = ""
    for file_name in files:
        file_path = os.path.join(FILES_DIR, file_name)
        if file_name.endswith(".pdf"):
            combined_text += extract_text_from_pdf(file_path) + "\n"
        elif file_name.endswith(".docx"):
            combined_text += extract_text_from_docx(file_path) + "\n"
        else:
            continue
    
    # Use NLP model to find the answer
    result = qa_pipeline(question=question, context=combined_text)
    return {"question": question, "answer": result["answer"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)