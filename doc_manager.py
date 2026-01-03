import os
import time
import hashlib
from typing import Optional
import litellm
import chromadb
from chromadb.config import Settings
from chroma_client import collection

from chroma_client import collection, CHROMA_DIR
print(f"📍 Utilise le chemin : {CHROMA_DIR}")
print(f"📊 Documents : {collection.count()}")

os.environ["MISTRAL_API_KEY"] = "4kkG27Ccz0aOzibls4GuGanWTp6FyoJE"

# =========================
# CONFIG
# =========================

CHROMA_DIR = "./chroma_txt_db"
COLLECTION_NAME = "txt_documents"


# =========================
# UTILS
# =========================

def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class Document:
    def __init__(self, id: int, content: str, embedding=None):
        self.id = id
        self.content = content
        self.hash = compute_hash(content)
        self.embedding = embedding




# =========================
# CORE FUNCTIONS
# =========================

def get_next_id(collection) -> int:
    data = collection.get()
    ids = [int(i) for i in data["ids"] if i.isdigit()]
    return max(ids) + 1 if ids else 0


def document_exists(collection, content: str) -> bool:
    content_hash = compute_hash(content)
    existing = collection.get(where={"hash": content_hash})
    return bool(existing["ids"])


def add_document_to_collection(
    collection,
    content: str
) -> Optional[Document]:

    if document_exists(collection, content):
        print(" Document déjà existant (hash)")
        return None

    doc_id = get_next_id(collection)

    embedding_response = litellm.embedding(
        model="mistral/mistral-embed",
        input=[content]
    )

    embedding = embedding_response["data"][0]["embedding"]

    document = Document(
        id=doc_id,
        content=content,
        embedding=embedding
    )

    collection.add(
        documents=[document.content],
        embeddings=[document.embedding],
        metadatas=[{"hash": document.hash}],
        ids=[str(document.id)]
    )

    print(f" Ajouté | id={doc_id} | hash={document.hash[:8]}...")
    return document


# =========================
# BULK INGESTION
# =========================

def ingest_txt_folder(folder_path: str, sleep_sec: float = 1.0):
    """
    Parcourt récursivement un dossier et ingère tous les .txt
    """

    if not os.path.isdir(folder_path):
        raise ValueError("Le chemin fourni n'est pas un dossier valide")

    print(f"\n Scan du dossier : {folder_path}\n")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith(".txt"):
                continue

            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if not content:
                    print(f"⏭ Fichier vide ignoré : {file}")
                    continue

                print(f"➡ Traitement : {file}")
                add_document_to_collection(collection, content)

                time.sleep(sleep_sec)

            except Exception as e:
                print(f" Erreur sur {file} : {e}")


# =========================
# MAINTENANCE
# =========================

def delete_document_by_id(doc_id: str) -> bool:
    existing = collection.get(ids=[doc_id])
    if existing["ids"]:
        collection.delete(ids=[doc_id])
        print(f" Document {doc_id} supprimé")
        return True
    return False


def list_documents(limit: int = 10):
    data = collection.get(include=["documents"])
    print("\n Documents stockés :\n")
    for doc_id, content in zip(data["ids"][:limit], data["documents"][:limit]):
        print(f"ID={doc_id} | {content[:200]}...")


def delete_all_documents():
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)
        print(f" {len(ids)} documents supprimés")
    else:
        print("ℹ Collection déjà vide")


FOLDER_PATH = "./scrap"

ingest_txt_folder(
    folder_path=FOLDER_PATH,
    sleep_sec=1.0
)

print("COUNT APRÈS =", collection.count())
print("✅ Ingestion terminée et persistée.")


# Ajoutez à la fin de doc_manager.py
import os
print("\n VÉRIFICATION:")
print(f"Dossier existe ? {os.path.exists(CHROMA_DIR)}")
print(f"Contenu : {os.listdir(CHROMA_DIR) if os.path.exists(CHROMA_DIR) else 'N/A'}")

