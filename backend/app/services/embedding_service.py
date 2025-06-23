import json
import spacy
import os
import numpy as np
from utils.file_utils import process_pdf_to_markdown

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
            context = process_pdf_to_markdown(file_path)

            # # Combine text, tables, and text from images into a single string
            # combined_text = context['text']

            # # Add tables to the combined text
            # for table in context['tables']:
            #     # Convert table (list of dictionaries) into Markdown-like format
            #     table_lines = [" | ".join(map(str, row.values())) for row in table]
            #     combined_text += "\n" + "\n".join(table_lines)

            # # Add placeholder for image text (if OCR is implemented later)
            # combined_text += "\n[Images extracted, OCR processing required]"

            document_store.append(context)

            embeddings_store.append(nlp(context).vector)

    # Convert embeddings to a NumPy array
    embeddings_store = np.array(embeddings_store)

    # Log the number of documents processed
    if document_store:
        print(f"Loaded {len(document_store)} documents.")

    else:
        print("No documents found in the specified directory.")

    return document_store, embeddings_store


def process_json_for_embedding(json_path: str):
    with open(json_path, "r") as f:
        content = json.load(f)

    combined = "\n".join(content.get("text", []))

    for table in content.get("tables", []):
        table_lines = [" | ".join(row) for row in table]
        combined += "\n" + "\n".join(table_lines)

    combined += "\n[Images extracted, OCR if needed]"

    return combined