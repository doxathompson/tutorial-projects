"""A layered task API built on WSGI and SQLite for educational transparency."""
from __future__ import annotations
import base64,hashlib,hmac,json,logging,os,secrets,sqlite3,time
from pathlib import Path
from wsgiref.simple_server import make_server
DB_PATH=Path(os.getenv("TASK_DB","tasks.db")); SECRET=os.getenv("TASK_SECRET",secrets.token_hex(32)).encode()
logging.basicConfig(format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',level=logging.INFO)
def connect(path:Path=DB_PATH):
    db=sqlite3.connect(path);db.executescript("""PRAGMA foreign_keys=ON; CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL); CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL CHECK(length(title)<=200), done INTEGER NOT NULL DEFAULT 0);""");return db
def hash_password(password:str,salt:bytes|None=None)->str:
    if len(password)<10:raise ValueError("password must contain at least 10 characters")
    salt=salt or secrets.token_bytes(16); digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1);return base64.urlsafe_b64encode(salt+digest).decode()
def verify_password(password:str,stored:str)->bool:
    raw=base64.urlsafe_b64decode(stored);return hmac.compare_digest(hash_password(password,raw[:16]),stored)
def token_for(user_id:int,expires:int|None=None)->str:
    payload=f"{user_id}.{expires or int(time.time())+3600}";signature=hmac.new(SECRET,payload.encode(),hashlib.sha256).hexdigest();return f"{payload}.{signature}"
def user_from_token(token:str)->int:
    try: uid,expiry,signature=token.split(".");expected=hmac.new(SECRET,f"{uid}.{expiry}".encode(),hashlib.sha256).hexdigest()
    except ValueError as exc:raise PermissionError("invalid token") from exc
    if not hmac.compare_digest(signature,expected) or int(expiry)<time.time():raise PermissionError("invalid or expired token")
    return int(uid)
def respond(start,status,payload):
    body=json.dumps(payload).encode();start(status,[("Content-Type","application/json"),("Content-Length",str(len(body)))]);return [body]
def application(env,start):
    try:
        path=env["PATH_INFO"];method=env["REQUEST_METHOD"];db=connect();length=int(env.get("CONTENT_LENGTH") or 0);data=json.loads(env["wsgi.input"].read(length) or b"{}")
        if path=="/health":return respond(start,"200 OK",{"status":"ok"})
        if path=="/register" and method=="POST":db.execute("INSERT INTO users(username,password_hash) VALUES (?,?)",(data["username"],hash_password(data["password"])));db.commit();return respond(start,"201 Created",{"created":True})
        if path=="/login" and method=="POST":
            row=db.execute("SELECT id,password_hash FROM users WHERE username=?",(data["username"],)).fetchone()
            if not row or not verify_password(data["password"],row[1]):raise PermissionError("bad credentials")
            return respond(start,"200 OK",{"token":token_for(row[0])})
        header=env.get("HTTP_AUTHORIZATION","");uid=user_from_token(header.removeprefix("Bearer "))
        if path=="/tasks" and method=="POST":db.execute("INSERT INTO tasks(user_id,title) VALUES (?,?)",(uid,data["title"]));db.commit();return respond(start,"201 Created",{"created":True})
        if path=="/tasks":rows=db.execute("SELECT id,title,done FROM tasks WHERE user_id=?",(uid,)).fetchall();return respond(start,"200 OK",{"tasks":[{"id":r[0],"title":r[1],"done":bool(r[2])} for r in rows]})
        return respond(start,"404 Not Found",{"error":"not found"})
    except PermissionError as exc:return respond(start,"401 Unauthorized",{"error":str(exc)})
    except (ValueError,KeyError,json.JSONDecodeError,sqlite3.IntegrityError) as exc:return respond(start,"400 Bad Request",{"error":str(exc)})
if __name__=="__main__":make_server("127.0.0.1",8080,application).serve_forever()

