from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader  # Updated imports
from langchain.vectorstores import FAISS  # Use FAISS instead of Chroma
from typing import List
from core.config import settings
from dotenv import load_dotenv
import os
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings


load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = None


    def process_document(self, file_path: str) -> None:
        """Process a single document and add it to vector store"""
        if not os.path.isfile(file_path):
            raise ValueError(f"File path {file_path} is not a valid file or url")
        
        loader = PyPDFLoader(file_path=file_path)
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

    def process_documents(self, texts: List[str]) -> None:
        """Process a list of text documents and add them to the vector store."""
        documents = [Document(page_content=text) for text in texts]
        
        if not self.vector_store:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
