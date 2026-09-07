# Personal Finance Web App

A small WSGI application backed by SQLite. It uses parameterized SQL and a
schema bootstrap, while avoiding a framework so the HTTP fundamentals remain
visible.

```bash
python app.py  # http://localhost:8000
python -m unittest discover -s tests -v
```

