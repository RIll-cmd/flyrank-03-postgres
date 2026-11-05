# Task API

Python and FastAPI provide CRUD endpoints and interactive documentation at `/docs`.

```sh
pip install -r requirements.txt
uvicorn app:app --reload
```

| Method | Path | Purpose |
|---|---|---|
| GET | /, /health | API information and health |
| GET | /tasks, /tasks/{id} | List or read |
| POST | /tasks | Create with `{"title":"Buy milk"}` |
| PUT | /tasks/{id} | Update `title` and/or `done` |
| DELETE | /tasks/{id} | Delete |

Missing or invalid input returns 400; unknown task IDs return 404.

Copy `.env.example` to `.env`, then run `docker compose up --build`. PostgreSQL data is stored in the named `postgres_data` volume. The app and routes are identical to the SQLite assignment; only the repository is replaced, with deployment configuration and initialization added.

To verify persistence: create a task, run `docker compose down`, run `docker compose up -d`, and retrieve the task with `GET /tasks`. Do not add `-v`, which removes the volume. This procedure has not yet been run: Docker's engine was unavailable during implementation.
