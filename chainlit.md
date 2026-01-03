# 🤖 Assistant RAG Chainlit + ChromaDB

Cet assistant est un **chatbot RAG (Retrieval-Augmented Generation)** basé sur **Chainlit**, **ChromaDB** et les modèles **Mistral** via **LiteLLM**.

Il permet de répondre aux questions des utilisateurs **uniquement à partir d’un corpus de documents texte (.txt)** ingérés dans une base vectorielle Chroma.

---

## 🧠 Fonctionnement général

1. 📂 Des fichiers `.txt` sont ingérés depuis un dossier (`./scrap`)
2. 🔢 Chaque document est transformé en **embedding vectoriel** (Mistral Embed)
3. 💾 Les documents + embeddings sont stockés dans **ChromaDB**
4. ❓ Lors d’une question utilisateur :

   * les documents les plus similaires sont recherchés
   * un **prompt contrôlé** est construit
   * le LLM répond **uniquement à partir du contexte fourni**

Si aucune information pertinente n’est trouvée, l’assistant renvoie un message standard.

---

## 🗂️ Architecture du projet

```
LLM_GENAI/
│
├── chroma_client.py      # Initialisation unique de ChromaDB (client + collection)
├── doc_manager.py        # Ingestion des fichiers texte (.txt)
├── rag_engine.py         # Recherche sémantique (similarité cosine)
├── main.py               # Application Chainlit (chat)
├── scrap/                # Dossier contenant les fichiers .txt à ingérer
├── chroma_txt_db/        # Base ChromaDB persistée (auto-générée)
└── README.md
```

---

## ⚙️ Prérequis

* Python **3.10+**
* Un environnement virtuel recommandé

### 📦 Dépendances principales

```bash
pip install chainlit chromadb litellm scikit-learn
```

---

## 🔑 Configuration

### Clé API Mistral

La clé API est définie via une variable d’environnement :

```python
os.environ["MISTRAL_API_KEY"] = "VOTRE_CLE_API"
```

⚠️ En production, **ne jamais hardcoder la clé**.

---

## 📥 Étape 1 — Ingestion des documents

1. Placer vos fichiers `.txt` dans le dossier :

```
./scrap
```

2. Lancer l’ingestion :

```bash
python doc_manager.py
```

3. Vérifier la sortie :

```text
COUNT APRÈS = X   (X > 0)
```

👉 Les documents sont automatiquement persistés dans `chroma_txt_db`.

---

## 💬 Étape 2 — Lancer l’assistant

```bash
chainlit run main.py
```

Puis ouvrir le navigateur à l’adresse indiquée par Chainlit.

---

## 🧪 Logique RAG

* **Seuil de similarité** :

```python
SCORE_THRESHOLD = 0.65
```

* Si aucun document ne dépasse ce seuil, la réponse est :

```
Je n'ai pas d'informations à ce sujet.
Merci de contacter la scolarité à scolarité@esilv.fr
```

---

## 🔐 Contraintes de sécurité

* Le LLM est **strictement contraint** à répondre à partir du contexte fourni
* Aucune hallucination autorisée hors documents
* Sources affichées après chaque réponse

---

## 🛠️ Dépannage courant

### ❌ "Aucun document trouvé dans la collection"

✔ Vérifier que :

* `doc_manager.py` a bien été exécuté
* le dossier `scrap` contient des `.txt`
* le chemin Chroma est **absolu** et partagé par tous les fichiers

### ❌ COUNT = 0 dans `main.py`

➡️ Supprimer `chroma_txt_db`, relancer l’ingestion, puis relancer Chainlit.

---

## ✅ Résumé

✔ Ingestion automatique de documents texte
✔ Recherche sémantique fiable
✔ Réponses contrôlées et sourcées
✔ Architecture claire et modulaire

---

💡 **Une fois l’ingestion faite, ne relancez que `chainlit run main.py`.**
