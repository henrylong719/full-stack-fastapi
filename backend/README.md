# Backend (FastAPI)

The API server for the full-stack application. Built with FastAPI, Pydantic v2, and PyJWT.

## Architecture

```text
app/
├── main.py           # FastAPI app, middleware, lifespan
├── models.py         # Pydantic request/response schemas
├── api/
│   ├── main.py       # Router aggregation
│   ├── deps.py       # Shared dependencies (auth, current user)
│   └── routes/
│       ├── login.py  # OAuth2 token endpoints
│       ├── users.py  # User CRUD (admin + self-service)
│       ├── items.py  # Item CRUD
│       ├── utils.py  # Health check, debug tools
│       └── private.py # Local-only debug endpoints
├── core/
│   ├── config.py     # Settings via pydantic-settings
│   ├── security.py   # Password hashing, JWT creation/verification
│   └── logging.py    # Logging configuration
└── crud/
    ├── users.py      # User data operations
    ├── items.py      # Item data operations
    └── seed.py       # Local-only seed data
```

## Key Features

- **Authentication**: OAuth2 password flow with JWT access tokens
- **Authorization**: Role-based access (superuser / regular user)
- **Validation**: Pydantic v2 models with field-level constraints
- **Password hashing**: Argon2 + Bcrypt via `pwdlib`
- **Security headers**: X-Content-Type-Options, X-Frame-Options, HSTS (production)
- **CORS**: Restricted to configured origins with specific methods/headers
- **OpenAPI**: Auto-generated docs, disabled in production
- **Structured logging**: Environment-aware request logging

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
cd backend
uv sync
```

## Running

```bash
# Development (with hot reload)
uv run uvicorn app.main:app --reload

# The API is served at http://localhost:8000
# Swagger UI: http://localhost:8000/docs (local only)
```

## Environment

Configuration is loaded from `../.env` (the project root). See the root README for the full variable reference.

Key settings:

| Variable       | Effect                                                |
| -------------- | ----------------------------------------------------- |
| `ENVIRONMENT`  | `local` enables seed data, debug endpoints, Swagger   |
| `SECRET_KEY`   | JWT signing — validated for strength in non-local envs |

## Testing

```bash
uv run pytest
```

Tests use an in-memory data store that resets between test functions via the `auto_reset` fixture.

```bash
# With verbose output
uv run pytest -v

# Single test file
uv run pytest tests/api/routes/test_items.py
```

## Linting

```bash
uv run ruff check .
uv run ruff format .
```

## API Endpoints

### Auth

| Method | Path                          | Auth | Description            |
| ------ | ----------------------------- | ---- | ---------------------- |
| POST   | `/api/v1/login/access-token`  | No   | Get JWT access token   |
| POST   | `/api/v1/login/test-token`    | Yes  | Verify token is valid  |

### Users

| Method | Path                          | Auth    | Description              |
| ------ | ----------------------------- | ------- | ------------------------ |
| GET    | `/api/v1/users/me`            | User    | Get current user profile |
| PATCH  | `/api/v1/users/me`            | User    | Update own profile       |
| PATCH  | `/api/v1/users/me/password`   | User    | Change own password      |
| GET    | `/api/v1/users/`              | Admin   | List all users           |
| POST   | `/api/v1/users/`              | Admin   | Create user              |
| GET    | `/api/v1/users/{id}`          | Admin   | Get user by ID           |
| PATCH  | `/api/v1/users/{id}`          | Admin   | Update user              |
| DELETE | `/api/v1/users/{id}`          | Admin   | Delete user              |

### Items

| Method | Path                          | Auth | Description                        |
| ------ | ----------------------------- | ---- | ---------------------------------- |
| GET    | `/api/v1/items/`              | User | List items (own or all for admin)  |
| POST   | `/api/v1/items/`              | User | Create item                        |
| GET    | `/api/v1/items/{id}`          | User | Get item (owner or admin)          |
| PATCH  | `/api/v1/items/{id}`          | User | Update item (owner or admin)       |
| DELETE | `/api/v1/items/{id}`          | User | Delete item (owner or admin)       |

### Utils

| Method | Path                          | Auth | Description              |
| ------ | ----------------------------- | ---- | ------------------------ |
| GET    | `/api/v1/utils/health-check`  | No   | Returns `{"status":"ok"}`|
| GET    | `/api/v1/utils/whoami`        | User | Returns current email    |
| GET    | `/api/v1/utils/debug-seed`    | No   | Seed data counts (local) |
