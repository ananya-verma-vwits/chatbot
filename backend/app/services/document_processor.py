from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader  # Updated imports
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS  # Use FAISS instead of Chroma
from typing import List, Optional
from core.config import settings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Did not find OPENAI_API_KEY. Please set it in the environment or .env file.")
        
        # OpenAIEmbeddings reads the API key from the OPENAI_API_KEY environment variable
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def process_document(self, file_path: str) -> None:
        """Process a single document and add it to vector store"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        if not self.vector_store:
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
        else:
            self.vector_store.add_documents(texts)

    def process_directory(self, directory: str = settings.DOCS_DIR) -> None:
        """Process all PDF documents in a directory"""
        loader = DirectoryLoader(directory, glob="**/*.pdf")
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        if not self.vector_store:
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
        else:
            self.vector_store.add_documents(texts)

    def query_documents(self, query: str, k: int = 4) -> List[str]:
        """Query the vector store for relevant documents"""
        if not self.vector_store:
            raise ValueError("Vector store is not initialized. Please process documents first.")
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]