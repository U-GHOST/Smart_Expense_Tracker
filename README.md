# Smart Expense Tracker
* A local expense management system that uses Large Language Models to provide intelligent financial insights without data leaving the local network.
---
## Features:
* Local-first Intelligence: Uses Ollama to analyze spending habits locally (no internet connection required).
* Semantic Search: Query your expenses in natural language (e.g. 'How much did I spend on Coffee this month?').
* Predictive Suggestions: Get AI-generated advice on where to cut costs based on historical data stored in the vector database.
* No Cloud, No API Architecture: Since everything is running locally, there is no need for API calls, with your financial data staying on the machine.
---
## Architecture:
* This system uses a RAG (Retrieval-Augmented Generation) workflow:
	1. Ingestion: Expenses are validated via Pydantic and stored as embeddings in ChromaDB.
	2. Retrieval: When you ask a question, the system finds relevant expense records.
	3. Augmentation: These records are fed into a local Ollama model.
	4. Generation: The AI provides a formatted suggestion or summary.
---
## Tech Stack
* Python 3.12.
* Ollama as the model orchestrator.
* ChromaDB for storage.
* Pydnatic for validation.
* Streamlit for interface.
---
## Getting Started
1. The system needs Ollama to be installed on the target machine, and an embedding and chat model to be downloaded (for the local inference).
2. Install dependencies (we recommend using `uv` to manage packages): `pip install -r requirements.txt` (`uv add -r requirements.txt` for `uv`).
3. Run the application with `streamlit run main.py`, head to `http://localhost:8501` and use the system.
