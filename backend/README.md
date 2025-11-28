**Backend README**

- **Project:**: Flask backend with PostgreSQL, Docker, and CI/CD.
- **Location:**: `backend/`

**Quick Start (Docker Compose)**

1. Create a `.env` file with your PostgreSQL credentials (or use defaults):
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=social_media
   DATABASE_URL=postgresql://postgres:postgres@db:5432/social_media
   ```

2. Build and run with Docker Compose (add a `docker-compose.yml` if needed):
   ```sh
   docker-compose up --build
   ```

**Quick Start (Docker only)**

1. Start a PostgreSQL container (example):
   ```sh
   docker run --name sweg-pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=social_media -p 5432:5432 -d postgres:15
   ```
2. Build and run backend:
   ```sh
   docker build -t sweg-backend ./backend
   docker run --env DATABASE_URL=postgresql://postgres:postgres@<host_or_container>:5432/social_media -p 5001:5001 sweg-backend
   ```

**Tests**

- Run the test suite with `pytest` (requires PostgreSQL running):
  ```sh
  pytest
  ```

**Files of interest**

- `backend/run.py`: application entry point.
- `backend/requirements.txt`: Python dependencies.
- `backend/app/`: application package (routes, models, DB helpers).
- `backend/Dockerfile`: container build instructions.
- `.github/workflows/docker-build-push.yml`: CI/CD pipeline.
- `backend/docs/openapi.yaml` and `backend/API_REFERENCE.md`: API docs.

**CI/CD**

- On push to `main`, GitHub Actions builds and pushes the backend Docker image to DockerHub.
  - Set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in your repo.

**Notes**

- The backend now requires a running PostgreSQL instance.
- All database code uses SQLAlchemy for maintainability.
- For local dev, you can still run with venv and `DATABASE_URL` set.

