# Contributing

## Branch Naming
- `feat/<module>/<description>` — new features
- `fix/<module>/<description>` — bug fixes
- `docs/<description>` — documentation
- `refactor/<module>/<description>` — refactoring

Modules: `ml`, `backend`, `frontend`, `rag`, `shared`, `infra`

## Commit Messages
Follow Conventional Commits:
- `feat(module): description`
- `fix(module): description`
- `docs: description`
- `test(module): description`
- `chore: description`

## Pull Requests
1. Create a feature branch from `main`
2. Make changes in your module's directory
3. Write/update tests
4. Open a PR using the template
5. Request review from the module owner

## Code Style
- **Python**: Follow PEP 8, use snake_case
- **TypeScript/React**: Use camelCase for variables, PascalCase for components
- **API routes**: Use kebab-case (e.g., `/api/v1/fraud-network`)
