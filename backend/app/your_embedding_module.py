import os
import spacy
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Initialize document store and embeddings store
document_store = []
embeddings_store = None

# def process_documents(files_dir):
#     """Process documents and generate embeddings."""
#     global document_store, embeddings_store
#     document_store = []
#     embeddings_store = []

#     for file_name in os.listdir(files_dir):
#         file_path = os.path.join(files_dir, file_name)
#         if file_name.endswith(".txt"):  # Example for text files
#             with open(file_path, "r", encoding="utf-8") as f:
#                 text = f.read()
#                 document_store.append(text)
#                 embeddings_store.append(nlp(text).vector)

#     embeddings_store = np.array(embeddings_store)
#     print(f"Loaded {len(document_store)} documents.")