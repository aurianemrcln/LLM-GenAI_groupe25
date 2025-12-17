# LLM-GenAI_groupe25

# ESILV Smart Assistant

ESILV Smart Assistant est un chatbot intelligent pour l’école d’ingénieurs **ESILV**, capable de répondre aux questions sur les programmes, admissions et cours, collecter des informations de contact, et coordonner plusieurs agents spécialisés pour gérer des requêtes complexes.

---

## Fonctionnalités

- Réponses aux questions sur ESILV (programmes, admissions, cours)
- Collecte de contacts pour suivi ou inscription
- Coordination multi-agents :
  - Agent RAG pour réponses factuelles
  - Agent Formulaire pour collecte d’informations
  - Agent Admin pour suivi et analytics
- Interface Chainlit : chat, upload de documents, visualisation admin

---

## Technologies

- **Frontend** : [Chainlit](https://chainlit.io/)  
- **LLM** : Ollama (local) ou Google Vertex AI (cloud)  
- **Vector DB** : FAISS, Milvus, Chroma ou Pinecone  
- **Parsing docs** : PyMuPDF, pdfplumber, python-docx  
- **Orchestration** : Python (FastAPI / LangChain style)

---

## Installation (local)

```bash
git clone https://github.com/votre-utilisateur/esilv-smart-assistant.git
cd esilv-smart-assistant
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
chainlit run chainlit_app/app.py
```
## Structure du projet

esilv-smart-assistant/
├─ ingestion/       # Scraping et parsing de documents
├─ embeddings/      # Génération d'embeddings
├─ vectorstore/     # FAISS/Milvus/Chroma
├─ agents/          # Orchestrateur et agents
├─ chainlit_app/    # Frontend Chainlit
├─ deployment/      # Docker / GCP
└─ README.md

## Sécurité & confidentialité

Les documents internes restent privés

Collecte de données conforme RGPD

Ollama local : sécuriser le serveur, ne pas exposer publiquement
