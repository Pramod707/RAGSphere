# RAGSphere 📚🤖

RAGSphere is a production-style Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents, index them into a vector database, and ask natural language questions grounded in the uploaded documents.

The application uses a local Ollama LLM, Qdrant as the vector database, Inngest for workflow orchestration, FastAPI as the backend, and Streamlit as the frontend.

---

## Features

- Upload PDF documents
- Automatic PDF parsing and chunking
- Local embedding generation using Ollama
- Store embeddings in Qdrant
- Semantic similarity search
- Context-aware answer generation
- Source attribution for every answer
- Event-driven ingestion using Inngest
- Fully local LLM (No OpenAI API required)

---

## Tech Stack

### Backend
- FastAPI
- Inngest
- Python

### LLM
- Ollama
- Qwen2.5:7B

### Embeddings
- nomic-embed-text

### Vector Database
- Qdrant

### Frontend
- Streamlit

### Libraries
- LangChain
- LlamaIndex
- Qdrant Client
- Pydantic

---

## Project Architecture

```
                +------------------+
                |   Streamlit UI   |
                +---------+--------+
                          |
                          v
                 FastAPI Backend
                          |
                          v
                 Inngest Workflow
                          |
      +-------------------+-------------------+
      |                                       |
      v                                       v
 Load PDF                             User Query
      |                                       |
 Chunk PDF                             Create Embedding
      |                                       |
 Generate Embeddings                   Search Qdrant
      |                                       |
 Store in Qdrant                     Retrieve Context
                                              |
                                              v
                                     Ollama (Qwen2.5)
                                              |
                                              v
                                       Final Response
```

---

## Folder Structure

```
RAGSphere/
│
├── docs/                  # Sample PDFs
├── uploads/               # Uploaded PDFs
├── qdrant_storage/        # Qdrant persistent storage
│
├── custom_type.py         # Pydantic models
├── data_loaders.py        # PDF loading, chunking & embeddings
├── vector_db.py           # Qdrant operations
├── main.py                # FastAPI + Inngest workflows
├── streamlit_app.py       # Frontend
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Workflow

### PDF Ingestion

```
Upload PDF
      ↓
FastAPI
      ↓
Inngest Event
      ↓
Read PDF
      ↓
Chunk Text
      ↓
Generate Embeddings
      ↓
Store in Qdrant
```

---

### Question Answering

```
User Question
      ↓
Generate Embedding
      ↓
Search Qdrant
      ↓
Retrieve Relevant Chunks
      ↓
Send Context to Ollama
      ↓
Generate Answer
      ↓
Display Sources
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/RAGSphere.git

cd RAGSphere
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download

https://ollama.com

Pull models

```bash
ollama pull qwen2.5:7b

ollama pull nomic-embed-text
```

Run Ollama

```bash
ollama serve
```

---

## Run Qdrant

```bash
docker run -d \
--name qdrantRagDB \
-p 6333:6333 \
-v qdrant_storage:/qdrant/storage \
qdrant/qdrant
```

---

## Run FastAPI

```bash
uv run uvicorn main:app --reload
```

---

## Run Inngest

```bash
npx inngest-cli@latest dev
```

---

## Run Streamlit

```bash
streamlit run streamlit_app.py
```

---
## Usage

1. Start the FastAPI server.
2. Start the Inngest development server.
3. Launch the Streamlit application.
4. Upload one or more PDF documents.
5. Ask questions about the uploaded documents.
6. The application retrieves relevant context from Qdrant and generates grounded responses using the local Ollama model.

## Future Improvements

- Multi-document support
- Hybrid Search
- Metadata filtering
- Conversation memory
- User authentication
- Docker Compose deployment
- Cloud deployment
- Citation highlighting
- Streaming responses
- Re-ranking

---

## Author

**Pramod Boddu**

GitHub: https://github.com/Pramod707

LinkedIn: https://www.linkedin.com/in/pramod7/

---

## License

MIT License