# Frontend — Unified Dashboard

**Owner:** Person 3 | Part of: Digital Public Safety Platform — ET AI Hackathon 2026

## Overview

Next.js 16 unified dashboard that integrates all four platform modules (Counterfeit Currency Detection, Fraud Network Intelligence, Scam Shield) into a single, accessible UI. Day 1 establishes the complete foundation: routing, layout system, design language, reusable components, dark mode, and tests. API integration follows in Day 2.

---

## Tech Stack

| Layer | Library |
|---|---|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript 5 |
| Styling | Tailwind CSS v4 |
| Icons | Lucide React |
| Theme | next-themes |
| Variants | class-variance-authority |
| Testing | Jest + React Testing Library |
| Linting | ESLint (Next.js config) |
| Formatting | Prettier |

---

## Folder Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout (ThemeProvider, ToastProvider)
│   ├── page.tsx            # Landing page (/)
│   ├── not-found.tsx       # 404 page
│   ├── error.tsx           # Global error boundary
│   ├── loading.tsx         # Root loading state
│   ├── dashboard/          # /dashboard
│   ├── scanner/            # /scanner
│   ├── fraud-network/      # /fraud-network
│   ├── scam-shield/        # /scam-shield
│   ├── settings/           # /settings
│   └── about/              # /about
├── components/
│   ├── layout/             # Sidebar, TopNav, Footer, PageHeader, Breadcrumb, DashboardLayout
│   └── ui/                 # Button, Card, Badge, StatCard, SearchBar, Modal, Alert,
│                           # Toast, Spinner, Skeleton, EmptyState, ErrorState, ThemeToggle
├── contexts/
│   └── ThemeContext.tsx     # next-themes provider wrapper
├── hooks/
│   ├── useTheme.ts          # Theme toggle + mounted guard
│   └── useSidebar.ts        # Sidebar open/close state
├── services/
│   └── api.ts              # Base fetch client + module-specific stubs (Day 2)
├── constants/
│   └── navigation.ts       # Nav items, APP_NAME, APP_VERSION
├── types/
│   └── index.ts            # NavItem, BreadcrumbItem, StatCardData, Toast types
└── lib/
    └── utils.ts            # cn() helper (clsx + tailwind-merge)

tests/                      # Jest + RTL test files
__mocks__/                  # Static asset mocks for Jest
```

---

## Installation

```bash
cd frontend
npm install
cp .env.example .env.local   # defaults to localhost:8000
```

---

## Run Commands

```bash
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Production build
npm run start        # Serve production build
```

---

## Testing

```bash
npm test                     # Run all tests
npm test -- --watch          # Watch mode
npm run test:coverage        # Coverage report
```

**Test coverage (Day 1):**
- Sidebar — rendering, active route, close handler, nav links
- TopNav — header, search, sidebar toggle, notifications, theme button
- Header — landmark, search, user avatar
- Breadcrumb — nav, items, home link, aria-current
- 404 Not Found — text, dashboard link, home link
- DashboardLayout — children, sidebar, footer, main#id
- Footer — landmark, platform name
- PageHeader — h1 title, description, actions slot
- Button — variants, loading, disabled, click
- Badge, Alert, Spinner, Skeleton, EmptyState, ErrorState, SearchBar, Card

---

## Linting & Formatting

```bash
npm run lint             # ESLint check
npm run format           # Prettier format
npm run format:check     # Prettier check (CI)
```

---

## Design System

**Theme:** Government technology — blue `#1d4ed8` / white on light, `#3b82f6` on dark.

**Design tokens** are CSS custom properties (`var(--primary)`, `var(--muted)`, etc.) defined in `globals.css` and mapped through the `@theme inline` block for Tailwind. Dark mode is implemented via the `.dark` class, toggled by `next-themes` with system preference detection and `localStorage` persistence.

**Components follow:**
- Tailwind v4 (no `tailwind.config.js` — configuration via `@theme inline` in CSS)
- `class-variance-authority` for component variants
- `cn()` utility for conditional class merging
- ARIA labels, semantic HTML, `role`, and `aria-current` throughout

---

## Routes

| Route | Page |
|---|---|
| `/` | Landing page with feature overview |
| `/dashboard` | Stats overview, recent alerts, module status |
| `/scanner` | Currency upload UI (Day 2 API integration pending) |
| `/fraud-network` | Graph placeholder + flagged nodes list |
| `/scam-shield` | Chat UI with sample RAG response + knowledge sources |
| `/settings` | API endpoint + notification settings (Day 2 persistence) |
| `/about` | Team, tech stack, project overview |

---

## Future Integration (Day 2)

- **`services/api.ts`** — stubs ready: `detectCurrency()`, `queryScamShield()`, `getFraudNetwork()`. Replace `throw` with real `fetch` calls.
- **Currency Scanner** — wire file upload to `POST /api/v1/currency/detect`.
- **Scam Shield chat** — wire text input to `POST /api/v1/scam-shield/query`, render streamed RAG response.
- **Fraud Network** — fetch Neo4j graph data and render with D3.js/Cytoscape.
- **Settings** — persist user preferences via a backend user preferences API.
- **Authentication** — add an auth provider and protected route middleware.
