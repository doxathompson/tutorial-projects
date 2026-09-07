# Production-Style Task API

A dependency-free JSON API emphasizing production concerns: password hashing,
bearer tokens, authorization, SQLite constraints, structured logs, and health
checks. In a real deployment, put it behind TLS and use a managed identity
provider rather than expanding this educational auth system.

```bash
TASK_SECRET='replace-me' python api.py
curl -X POST http://localhost:8080/register -d '{"username":"ada","password":"long-password"}'
python -m unittest discover -s tests -v
```

Endpoints: `GET /health`, `POST /register`, `POST /login`, and authenticated
`GET/POST /tasks` using `Authorization: Bearer <token>`.

