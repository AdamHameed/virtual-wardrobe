# virtual-closet

A portfolio-quality full-stack virtual closet application with:

- `frontend`: Next.js, TypeScript, App Router, Tailwind CSS, Zustand
- `backend`: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic
- `db`: PostgreSQL
- Docker Compose-first local development
- Persistent media uploads and database storage
- Searchable wardrobe management
- Outfit creation and planning foundations
- An explicitly AI-ready backend architecture without provider lock-in
- Railway-ready production container setup

## Services

The local stack runs three services:

- `frontend` on `http://localhost:3000`
- `backend` on `http://localhost:8000`
- `db` on `localhost:5432`

Useful backend URLs:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

## Deployment Modes

- Local development uses Docker Compose plus the dev-focused files [backend/Dockerfile.dev](/Users/adam/Downloads/Projects/virtual-wardrobe/backend/Dockerfile.dev) and [frontend/Dockerfile.dev](/Users/adam/Downloads/Projects/virtual-wardrobe/frontend/Dockerfile.dev).
- Railway deployment uses the production Dockerfiles at [backend/Dockerfile](/Users/adam/Downloads/Projects/virtual-wardrobe/backend/Dockerfile) and [frontend/Dockerfile](/Users/adam/Downloads/Projects/virtual-wardrobe/frontend/Dockerfile).

## Quick Start

1. Optional: copy example environment files if you want to override defaults.

```bash
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

2. Start the full stack.

```bash
make up
```

3. In a second terminal, run database migrations.

```bash
make migrate
```

4. Optional: load a demo user with sample items and an example outfit.

```bash
make seed-demo
```

5. Open the app.

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
Docs:     http://localhost:8000/docs
```

Demo credentials after seeding:

```text
Email:    demo@virtualcloset.dev
Password: demo12345
```

## Product Highlights

- Register or sign in with JWT-based authentication
- Add wardrobe items with local image uploads
- Search across item names, categories, colors, brands, and notes
- Create reusable outfits from saved clothing items
- Keep frontend auth state shared while leaving server collections local to each screen
- Preserve clean seams for future recommendation, auto-tagging, and wardrobe analysis engines

## Why This Docker Setup Is Reliable

- PostgreSQL has a real healthcheck using `pg_isready`
- The backend waits for the database before starting Uvicorn
- The frontend waits for the backend healthcheck before starting
- Postgres data and uploaded media are stored in named Docker volumes
- Source code is bind-mounted for fast local iteration

## Volumes

- `postgres_data`: PostgreSQL data persistence
- `backend_media`: uploaded clothing images
- `frontend_node_modules`: frontend dependency cache inside Docker

## Common Commands

Start everything:

```bash
make up
```

Stop everything:

```bash
make down
```

Tail logs:

```bash
make logs
```

Apply migrations:

```bash
make migrate
```

Create a new Alembic migration:

```bash
make makemigrations m="describe_change"
```

Open a shell in the backend container:

```bash
make backend-shell
```

Open a PostgreSQL shell:

```bash
make db-shell
```

Seed demo data:

```bash
make seed-demo
```

## Direct Docker Compose Commands

If you prefer raw Compose commands:

```bash
docker compose up --build
docker compose exec backend alembic upgrade head
docker compose logs -f
docker compose down
```

## Notes

- Docker Compose is the main local development workflow.
- The backend uses PostgreSQL only.
- Uploaded files are stored in the Docker `backend_media` volume and served by FastAPI at `/media/...`.
- The backend architecture is already structured for future AI-related extensions without adding provider integrations yet.

## Railway Deployment

Deploy this repo to Railway as three services:

1. PostgreSQL database
2. Backend service rooted at `backend/`
3. Frontend service rooted at `frontend/`

### Backend Service

- Root directory: `backend`
- Dockerfile: `backend/Dockerfile`
- Healthcheck path: `/api/v1/health`
- Pre-deploy command: `alembic upgrade head`

Recommended Railway variables:

```text
VC_APP_ENV=production
VC_DEBUG=false
VC_SECRET_KEY=<generate-a-long-random-secret>
VC_DATABASE_URL=${{Postgres.DATABASE_URL}}
VC_CORS_ORIGINS=https://<your-frontend-domain>
VC_MEDIA_ROOT=/data/media
VC_MEDIA_URL=/media
VC_ACCESS_TOKEN_EXPIRE_MINUTES=60
VC_JWT_ALGORITHM=HS256
```

Notes:

- The backend now normalizes Railway-style `postgres://` and `postgresql://` URLs into SQLAlchemy's `postgresql+psycopg://` format automatically.
- If you want uploaded images to persist across deployments, attach a Railway volume to the backend service and mount it at `/data`.

### Frontend Service

- Root directory: `frontend`
- Dockerfile: `frontend/Dockerfile`
- Healthcheck path: `/`

Recommended Railway variables:

```text
NEXT_PUBLIC_API_URL=https://<your-backend-domain>/api/v1
```

### Deployment Checklist

- Create the PostgreSQL service first
- Point `VC_DATABASE_URL` at the Railway Postgres service variable
- Set a real `VC_SECRET_KEY`
- Set `VC_CORS_ORIGINS` to the deployed frontend domain
- Set `NEXT_PUBLIC_API_URL` to the deployed backend domain plus `/api/v1`
- Add the backend pre-deploy command `alembic upgrade head`
- Attach a Railway volume to `/data` if you want persistent uploads

## Architecture Notes

### Frontend

- `frontend/lib/api/` owns typed API communication by domain: auth, clothing items, outfits, planner, and recommendations.
- `frontend/store/auth-store.ts` is intentionally the only shared global store because auth is true application state.
- Wardrobe items, outfit lists, form state, and search state remain local to the screen so server data does not become an accidental global cache.
- The dashboard is broken into smaller components to keep validation, empty states, and loading states easy to reason about.

### Backend

- FastAPI route handlers stay thin and delegate database access to repositories plus business logic to services.
- Authentication, recommendations, and weather are separated behind clean modules and typed contracts.
- The recommendation engine already uses an interface-driven design so a future AI-backed implementation can replace the rule-based engine without breaking the API contract.
- Placeholder AI-ready models and provenance fields are present for future auto-tagging, embeddings, and recommendation logging, but they are not wired into production flows yet.

## Interview-Friendly Talking Points

- The project separates transport, business logic, persistence, and UI state cleanly enough to discuss tradeoffs without hand-waving.
- The frontend demonstrates restraint with state management: Zustand is used where it adds value, not as a default cache for everything.
- The backend keeps a stable contract around recommendations and provenance so future AI features can be introduced without forcing a frontend rewrite.
