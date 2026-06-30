# RAG — Digital Arrest Scam Shield

**Owner:** Person 4

## Overview
RAG-based system to detect and explain digital arrest scams using LangChain and ChromaDB.

## Tech Stack
- LangChain
- ChromaDB
- FastAPI
- Python

## Setup
```bash
cd rag
pip install -r requirements.txt
```

## Directory Guide
- `documents/` — source documents for knowledge base
- `src/ingestion/` — document processing pipeline
- `src/retriever/` — vector search retrieval
- `src/chains/` — LangChain chains
- `src/agents/` — LangChain agents
- `src/prompts/` — prompt templates
