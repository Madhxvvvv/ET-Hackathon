# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Digital Public Safety Platform — a hackathon (ET AI Hackathon 2.0) monorepo split into four independent modules plus shared code. Each module is owned by one person, has its own dependencies/tests, and deploys separately. Most of the repo is **scaffold**: the RAG module is the only substantially implemented part today; `backend` has only a `/health` endpoint and empty router files; `ml` and `frontend` are directory skeletons.

## Module layout & boundaries

| Dir | Purpose | Stack | Status |
|---|---|---|---|
| `rag/` | Digital Arrest Scam Shield — document retrieval | LangChain + ChromaDB + sentence-transformers | Implemented (ingestion + retrieval pipeline) |
| `backend/` | API gateway + fraud network | FastAPI, (Neo4j planned) | `/health` only; routers are empty stubs |
| `ml/` | Counterfeit currency detection | PyTorch (planned) | Skeleton |
| `frontend/` | Unified dashboard | Next.js 14 App Router (planned) | Skeleton |
| `shared/` | Cross-module API schemas, constants, types | — | Empty `__init__.py` packages |

**Architectural rule:** modules never import each other directly. The backend is the single API gateway; ML and RAG are consumed via HTTP through it, not via Python imports. Cross-module contracts live in `shared/api_schemas/`. Changes to `shared/` or root config are coordinated across the team.

## Commands

Use the Makefile targets from the repo root:

```bash
make install-<module>   # backend | frontend | ml | rag
make dev-backend        # uvicorn app.main:app --reload --port 8000
make dev-rag            # uvicorn app.main:app --reload --port 8001 (note: rag/app not yet created)
make dev-frontend       # npm run dev
make test               # runs all module test suites
make test-<module>      # backend | frontend | ml | rag
make clean              # remove __pycache__, .pytest_cache, frontend build artifacts
```

Each Python module has its own `requirements.txt` and is run **from its own directory** (the Makefile `cd`s in first). Tests import via `configs.config` / `src....`, which only resolve when pytest runs from inside the module dir.

```bash
cd rag && pytest tests -v                        # all rag tests
cd rag && pytest tests/test_rag_foundation.py -v # single file
cd rag && pytest tests -k "chunk" -v             # single test by name
```

## RAG module (the implemented one)

Pipeline: `documents/raw/*.{pdf,txt,md}` → chunk → embed → persist to ChromaDB → retrieve.

- **Run ingestion:** `cd rag && python -m src.ingestion.ingest` (re-run whenever docs change; `vectordb/` is gitignored, so every clone must run this locally before querying).
- **Public retrieval contract:** `src/retriever/retriever.py::retrieve(query, k)` returns `list[RetrievedChunk]`. This signature is a cross-team contract (backend will wrap it in `/scam-shield/query`, Day-2 chatbot calls it directly) — **do not change it without flagging the team.**
- **Config is env-driven** (`rag/configs/config.py`): all paths, chunk sizes, and model names come from `RAG_*` env vars with defaults. Import config values from there rather than hardcoding.
- **Embedding provider is swappable** via `RAG_EMBEDDING_PROVIDER` (default `sentence-transformers`, local, no API key; also `openai`, `cohere`). `src/utils/embeddings.py::get_embedding_function()` is the only place a provider SDK is imported — keep it that way. It's `lru_cache`d, so the model loads once per process.
- `src/chains/`, `src/agents/`, `src/prompts/` are reserved for Day 2 (chatbot/agent) and currently empty.
- Tests **skip rather than fail** when offline (embedding/vector-store steps need model downloads), so CI doesn't block on network access — preserve this pattern when adding tests.

## Conventions

- Branches: `<type>/<module>/<description>` (e.g. `feat/rag/ingestion`); types `feat|fix|docs|refactor|test|chore`; modules `ml|backend|frontend|rag|shared|infra`.
- Commits: Conventional Commits — `feat(rag): add retriever`.
- Python 3.10+ (uses `from __future__ import annotations`, `X | None` syntax). Python files/functions snake_case, classes PascalCase. API routes kebab-case under `/api/v1/`. Env vars UPPER_SNAKE_CASE.
- Model weights, datasets, embeddings, and `vectordb/` are gitignored — never commit them.
