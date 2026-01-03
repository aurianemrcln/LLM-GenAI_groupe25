import os
import chromadb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_txt_db")
COLLECTION_NAME = "txt_documents"

client = chromadb.PersistentClient(
    path=CHROMA_DIR  
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

print(f" ChromaDB initialisé : {CHROMA_DIR}")
print(f" Documents dans la collection : {collection.count()}")