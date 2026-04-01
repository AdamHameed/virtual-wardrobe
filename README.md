# virtual-closet

A production-style monorepo starter for a virtual closet app with:

- `frontend`: Next.js, TypeScript, App Router, Tailwind CSS, Zustand
- `backend`: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic
- `db`: PostgreSQL
- Docker Compose-first local development workflow
- Local media uploads for clothing item images

## Project Structure

```text
virtual-closet/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── media/
│   └── tests/
├── frontend/
└── docker-compose.yml
```

## Quick Start

1. Optional: copy the example environment files if you want to override defaults:

```bash
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

2. Start the full stack with Docker Compose:

```bash
docker compose up --build
```

3. Run the initial database migration in a second terminal:

```bash
docker compose exec backend alembic upgrade head
```

4. Open the apps:

- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/api/v1/health`

## Development Workflow

Docker Compose is the primary local workflow. The default services are:

- `frontend`
- `backend`
- `db`

Hot reload is enabled for both app services through bind mounts.

## Uploads

Uploaded clothing images are stored locally in `backend/media/` and are served by the backend at `/media/...`.

## Useful Commands

Start services:

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```

Create a new Alembic migration:

```bash
docker compose exec backend alembic revision --autogenerate -m "describe_change"
```

Apply migrations:

```bash
docker compose exec backend alembic upgrade head
```

Run backend tests:

```bash
docker compose exec backend pytest
```

## Notes

- The backend is organized into API, services, repositories, and database layers to stay future-friendly for later AI features without introducing AI code yet.
- The frontend uses an environment-based API URL via `NEXT_PUBLIC_API_URL`.
- PostgreSQL is the only configured application database.
