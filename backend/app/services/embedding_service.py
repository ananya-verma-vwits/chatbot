import spacy
import os
import numpy as np
from utils.file_utils import extract_text_from_pdf, extract_text_from_docx

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Initialize document store and embeddings store
document_store = []
embeddings_store = None

def process_documents(files_dir: str):
    """Process documents and generate embeddings."""
    global document_store, embeddings_store

    # Ensure document_store and embeddings_store are initialized
    document_store = []
    embeddings_store = []

    # Iterate through files in the directory
    for file_name in os.listdir(files_dir):
        file_path = os.path.join(files_dir, file_name)
        if file_name.endswith(".pdf"):  # Example for PDF files
            text = extract_text_from_pdf(file_path)
            document_store.append(text)
            embeddings_store.append(nlp(text).vector)

    # Convert embeddings to a NumPy array
    embeddings_store = np.array(embeddings_store)

    # Log the number of documents processed
    if document_store:
        print(f"Loaded {len(document_store)} documents.")

    else:
        print("No documents found in the specified directory.")

    return document_store, embeddings_store

def process_latest_document(file_path: str):
    """Process the latest uploaded document and generate embeddings."""
    global document_store, embeddings_store

    # Clear existing document and embeddings stores
    document_store = []
    embeddings_store = []

    # Extract text based on file type
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")

    # Add the extracted text to the document store
    document_store.append(text)

    # Generate embeddings for the text
    embeddings_store = np.array([nlp(text).vector])

    print(f"Processed latest document: {file_path}")
    return document_store, embeddings_store