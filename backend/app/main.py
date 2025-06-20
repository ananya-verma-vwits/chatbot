import os
import shutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, chat
from services.ollama_service import start_ollama_server, stop_ollama_server
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="AVA Chatbot APIs",
    description="APIs for AVA Chatbot, including file upload, question answering, and chat functionalities.",
    version="1.0.0",
    root_path="/api", 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Start the Ollama server on application startup."""
    start_ollama_server()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the Ollama server on application shutdown."""
    stop_ollama_server()
    if os.path.exists(upload.FILES_DIR):
        shutil.rmtree(upload.FILES_DIR)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)