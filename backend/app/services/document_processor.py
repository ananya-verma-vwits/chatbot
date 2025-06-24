from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader  # Updated imports
from langchain.vectorstores import FAISS  # Use FAISS instead of Chroma
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from core.config import settings
from dotenv import load_dotenv
import os
from langchain.schema import Document
import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        self.embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-large")
        self.vector_store = None


    def process_document(self, file_path: str) -> None:
        """Process a single document and add it to vector store"""
        if not os.path.isfile(file_path):
            raise ValueError(f"File path {file_path} is not a valid file or url")
        
        loader = PyPDFLoader(file_path=file_path)
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        if not self.vector_store:
            logging.info("Creating vector store for the first time.")
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            logging.info(f"Adding {len(texts)} new documents to the vector store.")
        else:
            # Check if the documents are already in the vector store
            logging.info("Checking for duplicate documents in the vector store.")
            existing_docs = [doc.page_content for doc in self.vector_store.similarity_search("", k=len(self.vector_store.index_to_docstore_id))]
            new_texts = [text for text in texts if text.page_content not in existing_docs]
            
            if new_texts:
                logging.info(f"Adding {len(new_texts)} new documents to the vector store.")
                self.vector_store.add_documents(new_texts)
            else:
                logging.info("No new documents to add.")


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

document_processor = DocumentProcessor()