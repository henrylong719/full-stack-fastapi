# Full Stack FastAPI + Next.js

A full-stack web application inspired by the official [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template), adapted to use **Next.js (App Router)** for the frontend.

## Tech Stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Backend  | FastAPI, Pydantic, PyJWT, uvicorn             |
| Frontend | Next.js 16 (App Router), React 19, TypeScript |
| Styling  | Tailwind CSS v4, shadcn/ui, Radix UI          |
| Data     | TanStack Query, React Hook Form, Zod          |
| Tooling  | uv (Python), pnpm (Node), Ruff, ESLint        |

## Project Structure

```text
full-stack-fastapi/
├── backend/          # FastAPI API server
│   ├── app/
│   │   ├── api/      # Route handlers and dependencies
│   │   ├── core/     # Config, security, logging
│   │   ├── crud/     # Data access layer (users, items)
│   │   ├── models.py # Pydantic schemas
│   │   └── main.py   # App entrypoint
│   └── tests/        # pytest test suite
├── frontend/         # Next.js client
│   └── src/
│       ├── app/      # Pages (App Router)
│       ├── components/
│       ├── hooks/    # React Query hooks
│       └── lib/api/  # Typed API client
├── .env              # Backend environment variables
└── pyrightconfig.json
```

## Prerequisites

- Python 3.12+
- Node.js 20.9+ (required by Next.js 16)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [pnpm](https://pnpm.io/) (Node package manager)

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url> full-stack-fastapi
cd full-stack-fastapi
```

Copy the example environment files:

```bash
# Backend (project root)
cp .env.example .env

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

### 2. Start the backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**. Swagger docs are at `/api/v1/openapi.json` (local environment only).

### 3. Start the frontend

```bash
cd frontend
pnpm install
pnpm dev
```

The frontend will be available at **http://localhost:3000**.

## Environment Variables

### Backend (`.env` at project root)

| Variable                       | Default               | Description                              |
| ------------------------------ | --------------------- | ---------------------------------------- |
| `PROJECT_NAME`                 | `FastAPI App`         | Displayed in OpenAPI docs                |
| `ENVIRONMENT`                  | `local`               | `local`, `staging`, or `production`      |
| `SECRET_KEY`                   | *(local generated if omitted)* | JWT signing key (required and strong in prod) |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `60`                  | Token lifetime in minutes                |
| `ACCESS_TOKEN_COOKIE_NAME`     | `access_token`        | HttpOnly auth cookie name                |
| `CSRF_COOKIE_NAME`             | `csrf_token`          | CSRF companion cookie name               |
| `COOKIE_DOMAIN`                | *(unset)*             | Optional shared cookie domain, e.g. `.example.com` |
| `FRONTEND_HOST`                | `http://localhost:3000` | Added to CORS origins automatically    |
| `BACKEND_CORS_ORIGINS`         | `[]`                  | JSON array or comma-separated URLs       |

### Frontend (`frontend/.env.local`)

| Variable                   | Default                  | Description           |
| -------------------------- | ------------------------ | --------------------- |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000`  | Backend API base URL  |
| `NEXT_PUBLIC_CSRF_COOKIE_NAME` | `csrf_token`         | Must match backend `CSRF_COOKIE_NAME` |
| `NEXT_PUBLIC_APP_NAME`     | `App`                    | Display name (optional) |

## Default Accounts (Local Only)

Seed data is only loaded when `ENVIRONMENT=local`.

| Email               | Password         | Role       |
| ------------------- | ---------------- | ---------- |
| admin@example.com   | changethis123    | Superuser  |
| alice@example.com   | password123      | Regular    |

## Production Notes

This repo still uses an in-memory backend data store. Before production, replace
it with a real database and migrations. Non-local environments must set a strong
`SECRET_KEY`, a real `FRONTEND_HOST`, and exact CORS origins.

## Running Tests

```bash
# Backend
cd backend
uv run pytest

# Frontend
cd frontend
pnpm typecheck
pnpm lint
```

## License

MIT
