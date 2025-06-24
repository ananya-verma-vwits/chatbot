from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "AVA Chatbot"
    DOCS_DIR: str = str(Path(__file__).parent.parent.parent / "docs")
    VECTOR_STORE_DIR: str = str(Path(__file__).parent.parent.parent / "vectorstore")
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 200

settings = Settings()