import chainlit as cl
import os
import traceback
from chroma_client import collection, CHROMA_DIR
from litellm import completion
from rag_engine import get_similar_docs
import time 
import asyncio
# =========================
# CONFIGURATION
# =========================

os.environ["MISTRAL_API_KEY"] = "YOUR_API_KEY"

# Paramètres RAG
SCORE_THRESHOLD = 0.65
TOP_K_DOCS = 4

# System Prompt
SYSTEM_PROMPT = """Tu es l'assistant intelligent de l'ESILV (École Supérieure d'Ingénieurs Léonard de Vinci).

MISSION :
- Aider les étudiants, candidats et visiteurs à trouver des informations sur l'école
- Répondre précisément en te basant UNIQUEMENT sur la documentation officielle fournie
- Orienter vers les bons contacts si l'information n'est pas disponible

RÈGLES STRICTES :
1. N'invente JAMAIS d'informations : si tu ne trouves pas la réponse dans les documents, dis-le clairement
2. Réponds en français de manière claire, naturelle et professionnelle
3. Si besoin de plus d'infos, redirige vers : scolarité@esilv.fr
4. NE MENTIONNE PAS les sources dans ta réponse (pas de "[Document X]")
5. Réponds comme si tu connaissais naturellement ces informations
6. Structure ta réponse de manière claire et accessible

STYLE DE RÉPONSE :
- Ton conversationnel et direct
- Paragraphes fluides (évite les listes excessives sauf si vraiment nécessaire)
- Réponse complète mais concise

CONTEXTE À UTILISER :
{context}

Réponds maintenant à la question de l'utilisateur."""

# =========================
# INITIALISATION
# =========================

print("=" * 60)
print(" ESILV - Assistant Documentation")
print("=" * 60)
print(f" Base de données : {CHROMA_DIR}")
print(f" Documents chargés : {collection.count()}")
print(f" Seuil de similarité : {SCORE_THRESHOLD}")
print("=" * 60 + "\n")

# =========================
# HANDLERS CHAINLIT
# =========================

@cl.on_chat_start
async def start():

    await asyncio.sleep(2)
    """Message de bienvenue"""
    welcome_message = """# 👋 Bienvenue sur l'assistant ESILV !

Je suis là pour vous aider à trouver des informations sur :
- 📚 Les formations et programmes
- 🎓 Les admissions et inscriptions  
- 🌍 L'international et les échanges
- 💼 L'alternance et les stages
- 🏫 La vie étudiante
- 📍 Les campus (Paris, Nantes, Montpellier)

**Posez-moi votre question et je rechercherai dans la documentation officielle !**

*Si je n'ai pas l'information, je vous redirigerai vers le service compétent.*
"""
    await cl.Message(content=welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Traitement des questions utilisateur"""
    
    try:
        query = message.content.strip()

        if not query:
            await cl.Message(content="⚠️ Merci de poser une question.").send()
            return

        # Message de chargement
        loading_msg = cl.Message(content="🔍 Recherche dans la documentation...")
        await loading_msg.send()

        # =========================
        # PHASE 1 : RECHERCHE RAG
        # =========================
        
        docs = await get_similar_docs(query, collection, n=TOP_K_DOCS)

        # Filtrage par score de similarité
        context_docs = [
            doc for doc in docs
            if doc.get("similarity", 0) >= SCORE_THRESHOLD
        ]

        # =========================
        # PHASE 2 : GÉNÉRATION DE LA RÉPONSE
        # =========================

        if context_docs:
            # Construction du contexte avec les documents pertinents
            context = "\n\n".join([
                f"[Document {i+1}]\n{doc['document']}"
                for i, doc in enumerate(context_docs)
            ])
            
            user_prompt = f"""QUESTION DE L'UTILISATEUR :
{query}

Réponds en te basant UNIQUEMENT sur les documents ci-dessus."""

            system_content = SYSTEM_PROMPT.format(context=context)
        
        else:
            # Aucun document pertinent trouvé
            system_content = SYSTEM_PROMPT.format(
                context="AUCUN DOCUMENT PERTINENT TROUVÉ"
            )
            user_prompt = f"""QUESTION DE L'UTILISATEUR :
{query}

Tu dois répondre : "Je n'ai pas trouvé d'informations sur ce sujet dans la documentation disponible. Pour plus de détails, je vous invite à contacter la scolarité à scolarité@esilv.fr."
"""

        # Suppression du message de chargement
        await loading_msg.remove()

        # =========================
        # PHASE 3 : STREAMING LLM
        # =========================

        response_msg = cl.Message(content="")
        await response_msg.send()

        # Appel LLM avec streaming
        stream = completion(
            model="mistral/mistral-large-2512",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_prompt}
            ],
            stream=True,
            temperature=0.3  # Réponses plus factuelles
        )

        full_response = ""
        
        for chunk in stream:
            if chunk and "choices" in chunk:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                
                if content:
                    full_response += content
                    await response_msg.stream_token(content)

        await response_msg.update()

    except Exception as e:
        traceback.print_exc()
        error_msg = f""" **Une erreur est survenue**

Détails : `{str(e)}`

Merci de contacter le support technique ou de réessayer."""
        await cl.Message(content=error_msg).send()


# =========================
# FONCTIONS UTILITAIRES
# =========================

@cl.on_chat_end
async def end():
    """Message de fin de session"""
    print(" Session terminée")
