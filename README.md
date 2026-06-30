# Digital Public Safety Platform

> AI-powered platform for digital public safety — counterfeit currency detection, fraud network intelligence, scam shield, and a unified dashboard.

## Repository Structure

```
ET-Hackathon/
├── .github/                        # GitHub templates & CI
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── workflows/
│
├── backend/                        # API Gateway & Fraud Network (Person 2)
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── routers/                # API route handlers
│   │   │   ├── currency.py         # Counterfeit detection endpoints
│   │   │   ├── fraud.py            # Fraud network endpoints
│   │   │   └── scam_shield.py      # Scam shield endpoints
│   │   ├── services/               # Business logic layer
│   │   ├── schemas/                # Pydantic request/response models
│   │   ├── models/                 # Database ORM models
│   │   ├── middleware/             # Auth, CORS, logging middleware
│   │   ├── database/              # DB connections & migrations
│   │   ├── config/                # App configuration
│   │   └── utils/                 # Backend utilities
│   ├── tests/
│   ├── logs/
│   ├── requirements.txt
│   └── README.md
│
├── ml/                             # Counterfeit Currency Detection (Person 1)
│   ├── datasets/
│   │   ├── raw_images/            # Original currency images
│   │   ├── augmented/             # Augmented training images
│   │   ├── train/                 # Training split
│   │   ├── validation/            # Validation split
│   │   └── test/                  # Test split
│   ├── models/                    # Saved model weights (.pt/.pth)
│   ├── src/
│   │   ├── training/             # Training scripts & pipelines
│   │   ├── inference/            # Inference & prediction logic
│   │   └── utils/                # Data loading, augmentation helpers
│   ├── configs/                  # Hyperparameters, model configs
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── rag/                            # Digital Arrest Scam Shield (Person 4)
│   ├── documents/                 # Source knowledge base docs
│   ├── embeddings/                # Generated embeddings (not committed)
│   ├── vectordb/                  # ChromaDB persistent storage
│   ├── src/
│   │   ├── ingestion/            # Document processing pipeline
│   │   ├── retriever/            # Vector search & retrieval
│   │   ├── prompts/              # Prompt templates
│   │   ├── chains/               # LangChain chains
│   │   ├── agents/               # LangChain agents
│   │   └── utils/                # RAG utilities
│   ├── configs/                  # RAG configuration
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                       # Unified Dashboard (Person 3)
│   ├── src/
│   │   ├── app/                   # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── layouts/           # Page layouts, navigation
│   │   │   ├── ui/                # Reusable UI primitives
│   │   │   ├── dashboard/         # Main dashboard views
│   │   │   ├── currency/          # Counterfeit detection UI
│   │   │   ├── fraud/             # Fraud network visualization
│   │   │   └── scam-shield/       # Scam shield chat interface
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── contexts/              # React context providers
│   │   ├── services/              # API client functions
│   │   ├── styles/                # Global styles, Tailwind config
│   │   ├── assets/                # Static assets (icons, images)
│   │   ├── types/                 # TypeScript type definitions
│   │   └── utils/                 # Frontend utilities
│   ├── public/
│   ├── tests/
│   └── README.md
│
├── shared/                         # Shared code (All members)
│   ├── api_schemas/               # Cross-module API contracts
│   ├── constants/                 # Shared constants & enums
│   ├── config/                    # Environment configuration
│   ├── utils/                     # Common utility functions
│   ├── types/                     # Shared type definitions
│   └── README.md
│
├── docs/                           # Documentation
│   ├── architecture/              # Architecture decision records
│   ├── diagrams/                  # System & flow diagrams
│   ├── api/                       # API documentation
│   ├── meeting_notes/             # Team meeting notes
│   ├── research/                  # Research & references
│   └── presentation/             # Hackathon presentation materials
│
├── deployment/                     # Deployment configs
│   ├── render/                    # Render.com configs
│   ├── nginx/                     # Reverse proxy config
│   └── kubernetes/                # K8s manifests
│
├── scripts/                        # Automation scripts
│   ├── setup.sh
│   └── seed_db.sh
│
├── configs/                        # Global configuration files
├── tests/                          # Integration tests
│   └── integration/
│
├── .env.example                    # Environment variable template
├── .gitignore
├── Makefile                        # Build & dev commands
├── CONTRIBUTING.md                 # Contribution guidelines
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

---

## Team Ownership

| Folder | Owner | Role |
|--------|-------|------|
| `ml/` | **Person 1** | Counterfeit Currency Detection — model training, inference |
| `backend/` | **Person 2** | API Gateway & Fraud Network Intelligence — FastAPI, Neo4j |
| `frontend/` | **Person 3** | Unified Dashboard — Next.js, React, Tailwind |
| `rag/` | **Person 4** | Digital Arrest Scam Shield — LangChain, ChromaDB |
| `shared/` | **All** | Shared schemas, constants, utils (coordinate changes) |
| `docs/` | **Person 3** (lead) | Documentation & presentation |
| `deployment/` | **Person 2** (lead) | Render, Vercel, infra, CI/CD |
| `.github/` | **Person 2** (lead) | GitHub workflows & templates |

---

## Why This Architecture Is Scalable

1. **Module isolation** — Each module (`ml/`, `backend/`, `rag/`, `frontend/`) is self-contained with its own dependencies and tests. Adding a new module means adding a new top-level directory.

2. **Independent deployability** — Backend and RAG deploy to Render as separate services, frontend deploys to Vercel. Each service can scale independently.

3. **Clear API boundaries** — `shared/api_schemas/` defines contracts between modules. Backend acts as the API gateway, so ML and RAG don't need to know about the frontend, and vice versa.

4. **No cross-module imports** — ML and RAG are consumed via API calls through the backend, not direct Python imports. This allows swapping implementations without breaking other modules.

5. **Data pipeline separation** — ML datasets, RAG documents, and vector stores are isolated and gitignored, supporting different storage backends as data grows.

---

## Avoiding Merge Conflicts

Each team member works almost exclusively in their own directory:

| Person | Primary Directory | Touches Shared? |
|--------|------------------|-----------------|
| Person 1 | `ml/` | Rarely — only `shared/api_schemas/` for inference request/response |
| Person 2 | `backend/` | Yes — defines API schemas in `shared/`, manages deployment configs |
| Person 3 | `frontend/` | Rarely — reads `shared/types/` for API types |
| Person 4 | `rag/` | Rarely — only `shared/api_schemas/` for RAG request/response |

**Rules to avoid conflicts:**
- Never edit files outside your module without communicating first
- Changes to `shared/` require a quick team sync
- Person 2 owns deployment configs — others request changes via PR
- Each module has its own `requirements.txt` / `package.json`

---

## Git Branching Strategy

```
main                          # Always deployable
├── feat/ml/model-training    # Person 1
├── feat/backend/fraud-api    # Person 2
├── feat/frontend/dashboard   # Person 3
├── feat/rag/ingestion        # Person 4
```

**Branch naming:** `<type>/<module>/<description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Modules: `ml`, `backend`, `frontend`, `rag`, `shared`, `infra`

**Commit messages:** Conventional Commits — `feat(backend): add fraud detection endpoint`

**Workflow:**
1. Pull latest `main`
2. Create feature branch
3. Work in your module
4. Open PR, request review from module owner
5. Squash merge to `main`

---

## Recommended Initialization Order

| Order | Person | First Task |
|-------|--------|------------|
| 1 | **Person 2** | Initialize FastAPI app, set up Neo4j connection, create `/health` endpoint, configure Render deployment |
| 2 | **Person 3** | Run `npx create-next-app` inside `frontend/`, set up Tailwind, create basic layout |
| 3 | **Person 1** | Set up PyTorch environment, write data loading utilities, configure augmentation pipeline |
| 4 | **Person 4** | Set up LangChain + ChromaDB, write document ingestion pipeline, create basic retriever |

**Why this order:** Person 2 starts first because the backend is the integration hub — others need API endpoints to connect to. Person 3 starts the frontend scaffold early so UI work can begin in parallel. Persons 1 and 4 can work fully independently on their ML/RAG pipelines.

---

## Naming Conventions

| Domain | Convention | Example |
|--------|-----------|---------|
| **Folders** | snake_case (Python), kebab-case (React components) | `raw_images/`, `scam-shield/` |
| **Python files** | snake_case | `fraud_service.py` |
| **Python classes** | PascalCase | `FraudDetector` |
| **Python functions/vars** | snake_case | `detect_fraud()` |
| **React components** | PascalCase files & names | `DashboardCard.tsx` |
| **React hooks** | camelCase with `use` prefix | `useAuth.ts` |
| **TypeScript types** | PascalCase | `FraudNode` |
| **API routes** | kebab-case, versioned | `/api/v1/fraud-network` |
| **Git branches** | kebab-case | `feat/backend/fraud-api` |
| **Commits** | Conventional Commits | `feat(ml): add augmentation pipeline` |
| **Environment vars** | UPPER_SNAKE_CASE | `NEO4J_URI` |

---

## Assumptions

1. All Python modules will use Python 3.10+
2. Frontend uses Next.js 14 with App Router
3. Backend serves as the single API gateway — ML and RAG are called internally, not exposed directly
4. Neo4j is used only by the fraud network module
5. ChromaDB is used only by the RAG module
6. Model weights and datasets are NOT committed to git (gitignored)
7. Team members will communicate before changing `shared/` or root config files
8. Backend and RAG deploy to Render; frontend deploys to Vercel

---

## Recommended Improvements Before Implementation

1. **Set up a shared Postman/Bruno collection** — Define API contracts early so frontend and backend can develop in parallel using mocks
2. **Add pre-commit hooks** — Use `pre-commit` with `ruff` (Python) and `eslint`/`prettier` (TypeScript) for consistent formatting
3. **Create GitHub Actions CI** — Basic pipeline: lint + test on PR for each module
4. **Define API versioning** — All routes under `/api/v1/` from day one
5. **Set up a shared Figma/wireframe** — Person 3 should have UI mockups before coding
6. **Add health check endpoints** — Every service should expose `/health` for Render health checks
7. **Consider using pnpm workspaces** — If frontend grows, this helps manage shared packages

---

## Quick Start

```bash
# Clone the repo
git clone <repo-url> && cd ET-Hackathon

# Copy environment file
cp .env.example .env

# Run individual modules
make install-backend && make dev-backend
make install-frontend && make dev-frontend
make install-ml
make install-rag && make dev-rag
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
