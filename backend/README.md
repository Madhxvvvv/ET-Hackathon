# Backend — API Gateway & Fraud Network Intelligence

**Owner:** Person 2

## Modules Served
- Counterfeit Currency Detection API (routes for ML inference)
- Fraud Network Intelligence (Neo4j graph queries)
- Scam Shield API (routes for RAG queries)

## Tech Stack
- FastAPI
- Neo4j
- PostgreSQL

## Deployment
Deployed on **Render** as a web service.

## Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
