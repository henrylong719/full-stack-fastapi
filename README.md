# Full Stack FastAPI + Next.js

A full-stack web application inspired by the official [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template), adapted to use **Next.js (App Router)** for the frontend.

## Tech Stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Backend  | FastAPI, Pydantic, PyJWT, MySQL, uvicorn      |
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
│   │   ├── crud/     # Service layer for auth/users/items
│   │   ├── db/       # MySQL connection + schema management
│   │   ├── models.py # Pydantic schemas
│   │   ├── repositories/ # MySQL persistence implementations
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
- Node.js 18+ (LTS recommended)
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

The backend uses MySQL for persistence, so start a MySQL server and set the `MYSQL_*` variables in the root `.env` before launching the API.

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
| `SECRET_KEY`                   | *(random)*            | JWT signing key (must be strong in prod) |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `60`                  | Token lifetime in minutes                |
| `FRONTEND_HOST`                | `http://localhost:3000` | Added to CORS origins automatically    |
| `BACKEND_CORS_ORIGINS`         | `[]`                  | JSON array or comma-separated URLs       |
| `MYSQL_HOST`                   | `127.0.0.1`           | MySQL host                               |
| `MYSQL_PORT`                   | `3306`                | MySQL port                               |
| `MYSQL_USER`                   | `root`                | MySQL username                           |
| `MYSQL_PASSWORD`               | *(empty)*             | MySQL password                           |
| `MYSQL_DATABASE`               | `full_stack_fastapi`  | MySQL schema/database name               |
| `MYSQL_CONNECT_TIMEOUT`        | `10`                  | Connection timeout in seconds            |
| `MYSQL_AUTO_CREATE_DATABASE`   | `false`               | Creates the MySQL database if missing    |
| `MYSQL_AUTO_CREATE_TABLES`     | `true`                | Creates `users` and `items` tables on startup |
| `MYSQL_SEED_LOCAL_DATA`        | `true`                | Seeds local demo users/items into MySQL  |

### Frontend (`frontend/.env.local`)

| Variable                   | Default                  | Description           |
| -------------------------- | ------------------------ | --------------------- |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000`  | Backend API base URL  |
| `NEXT_PUBLIC_APP_NAME`     | `App`                    | Display name (optional) |

## Default Accounts (Local Only)

Seed data is only loaded when `ENVIRONMENT=local`.

| Email               | Password         | Role       |
| ------------------- | ---------------- | ---------- |
| admin@example.com   | changethis123    | Superuser  |
| alice@example.com   | password123      | Regular    |

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
