# SoccerPredictionLeague

## Setup

```bash
cp .env.example .env   # fill in your DATABASE_URL
pip install -r requirements.txt
```

Start PostgreSQL (Docker):

```bash
docker run -d \
  --name soccerdb \
  -e POSTGRES_USER=soccer \
  -e POSTGRES_PASSWORD=soccer \
  -e POSTGRES_DB=soccerdb \
  -p 5432:5432 \
  postgres:16
```

## Running the app

```bash
uvicorn app.main:app --reload
```

## Database migrations

| Command | What it does |
|---------|-------------|
| `alembic upgrade head` | Apply all pending migrations (run this after pulling new changes) |
| `alembic downgrade base` | Revert all migrations back to an empty database |
| `alembic downgrade -1` | Undo only the most recent migration |
| `alembic revision --autogenerate -m "describe change"` | Generate a new migration from your model changes |
| `alembic history` | Show the full migration history |
| `alembic current` | Show which migration the database is currently at |

### Workflow when you change a model

1. Edit or add a model class in `app/models/`
2. Import it in `app/models/__init__.py` so Alembic can see it
3. `alembic revision --autogenerate -m "add user table"`
4. Review the generated file in `migrations/versions/`
5. `alembic upgrade head`
