import json
from sklearn.metrics.pairwise import cosine_similarity
from litellm import completion, embedding
from chroma_client import collection

async def get_similar_docs(query, collection, n=4):
    try:
        # Embedding de la requête
        query_vec = embedding(
            model="mistral/mistral-embed",
            input=query
        )["data"][0]["embedding"]

        # Récupération des documents et embeddings
        all_docs = collection.get(include=["documents", "embeddings"])

        # Vérifie si la collection contient des documents
        if not all_docs["documents"]:
            print("[DEBUG] Aucun document trouvé dans la collection.")
            return []

        # Calcul de la similarité entre la requête et chaque document
        similitudes = [
            {
                "document": doc,
                "similarity": cosine_similarity([query_vec], [emb])[0][0]
            }
            for doc, emb in zip(all_docs["documents"], all_docs["embeddings"])
        ]

        # Tri des résultats par similarité décroissante
        similitudes.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Retourne les n meilleurs résultats
        return similitudes[:n]
        
    except Exception as e:
        # Gestion des erreurs pour éviter que l'exécution se bloque
        print(f"[ERROR] Erreur dans get_similar_docs: {e}")
        return []
