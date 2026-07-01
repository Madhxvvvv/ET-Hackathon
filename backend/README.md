# Backend — API Gateway

**Owner:** Person 2

The backend is a FastAPI application that acts as the API gateway for all three AI modules: Counterfeit Currency Detection, Fraud Network Intelligence, and Scam Shield.

## Tech Stack
- **FastAPI** — REST API + OpenAPI docs
- **Pydantic v2** — request/response validation
- **Neo4j** — fraud network graph database (Day 2)
- **Python 3.12+**

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `false` | Enable debug logging |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection URI |
| `NEO4J_USER` | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | `password` | Neo4j password |
| `ML_SERVICE_URL` | `http://localhost:8001` | ML inference service URL (Day 2) |
| `RAG_SERVICE_URL` | `http://localhost:8002` | RAG service URL (Day 2) |

Copy `.env.example` to `.env` and fill in values for local development.

## API Routes

| Method | Path | Status | Description |
|---|---|---|---|
| `GET` | `/health` | ✅ Live | Health check |
| `POST` | `/api/v1/currency/detect` | 🔜 Day 2 | Currency image classification |
| `GET` | `/api/v1/fraud-network/graph` | 🔜 Day 2 | Full Neo4j graph |
| `GET` | `/api/v1/fraud-network/nodes/{id}` | 🔜 Day 2 | Single node detail |
| `POST` | `/api/v1/scam-shield/query` | 🔜 Day 2 | RAG-grounded Q&A |

## Running Tests

```bash
cd backend
pytest tests/ -v
```

21 tests covering health, CORS config, input validation (422s), and stub contracts (501s).
