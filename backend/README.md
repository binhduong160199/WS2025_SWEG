**Backend README**

- **Project:**: Minimal Flask backend for the course project.
- **Location:**: `backend/`

**Quick Start**

- **Create or activate venv (optional):** Use the workspace venv or create a new one.
  - Example (PowerShell):
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
- **Install dependencies:**
  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
  ```
- **Run the server:**
  ```powershell
  .\.venv\Scripts\python.exe .\backend\run.py
  ```
  The app listens on `0.0.0.0:5000` by default (development server, `debug=True`).
  - **Swagger UI:** once the server is running, open `http://localhost:5000/api/docs` to view the interactive API documentation (served from `flask-swagger-ui`).


**Tests**

- Run the test suite with `pytest`:
  ```powershell
  .\.venv\Scripts\python.exe -m pytest -q
  ```

**Files of interest**

- `backend/run.py`: application entry point.
- `backend/requirements.txt`: pinned Python dependencies.
- `backend/app/`: application package (`create_app`, routes, models, DB helpers).
- `backend/docs/openapi.yaml` and `backend/API_REFERENCE.md`: API documentation.

- **Swagger UI endpoint:** `GET /api/docs` serves the interactive Swagger UI (OpenAPI) when the server is running.

**Notes & Recommendations**

- This repository uses a development server (Flask `debug=True`). For production, use a WSGI server such as `gunicorn` or `waitress` and set `debug=False`.
- If you create a new virtual environment, re-run the `pip install` step.

