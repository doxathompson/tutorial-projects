"""Minimal finance web app: WSGI transport around a tested SQLite core."""
from __future__ import annotations
import html, sqlite3
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
DB=Path("finance.db")
def connect(path: Path=DB) -> sqlite3.Connection:
    db=sqlite3.connect(path); db.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY, description TEXT NOT NULL, cents INTEGER NOT NULL CHECK(cents > 0))"); return db
def add_transaction(db: sqlite3.Connection, description: str, cents: int) -> None:
    if not description.strip() or cents<=0: raise ValueError("description and positive amount required")
    # Placeholders prevent user input from becoming executable SQL.
    db.execute("INSERT INTO transactions(description,cents) VALUES (?,?)",(description.strip(),cents)); db.commit()
def application(environ,start_response):
    db=connect()
    if environ["REQUEST_METHOD"]=="POST":
        length=int(environ.get("CONTENT_LENGTH") or 0); form=parse_qs(environ["wsgi.input"].read(length).decode()); add_transaction(db,form["description"][0],round(float(form["amount"][0])*100))
    rows=db.execute("SELECT description,cents FROM transactions ORDER BY id DESC").fetchall(); db.close()
    items="".join(f"<li>{html.escape(d)} — ${c/100:.2f}</li>" for d,c in rows)
    body=f"<h1>Transactions</h1><form method=post><input name=description required><input name=amount type=number min=.01 step=.01 required><button>Add</button></form><ul>{items}</ul>".encode()
    start_response("200 OK",[("Content-Type","text/html; charset=utf-8"),("Content-Length",str(len(body)))]); return [body]
if __name__=="__main__": make_server("127.0.0.1",8000,application).serve_forever()

