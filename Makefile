.PHONY: install dev test lint build clean

# Backend
install-backend:
	cd backend && pip install -r requirements.txt

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

test-backend:
	cd backend && pytest tests/

# Frontend
install-frontend:
	cd frontend && npm install

dev-frontend:
	cd frontend && npm run dev

test-frontend:
	cd frontend && npm test

# ML
install-ml:
	cd ml && pip install -r requirements.txt

test-ml:
	cd ml && pytest tests/

# RAG
install-rag:
	cd rag && pip install -r requirements.txt

dev-rag:
	cd rag && python -m src.ingestion.ingest

test-rag:
	cd rag && pytest tests/

# All
install: install-backend install-frontend install-ml install-rag

test: test-backend test-frontend test-ml test-rag

dev:
	@echo "Run each service in a separate terminal:"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"
	@echo "  make dev-rag"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf frontend/.next frontend/node_modules

