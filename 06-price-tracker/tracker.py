"""Record numeric observations and alert only on meaningful changes."""
from __future__ import annotations
import argparse,json,sqlite3
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
def fetch(url: str, field: str) -> float:
    request=Request(url,headers={"User-Agent":"learning-price-tracker/1.0"})
    with urlopen(request,timeout=15) as response: data=json.load(response)
    return float(data[field])
def connect(path: Path) -> sqlite3.Connection:
    db=sqlite3.connect(path); db.execute("CREATE TABLE IF NOT EXISTS observations(url TEXT, value REAL, observed_at TEXT)"); return db
def record(db: sqlite3.Connection,url: str,value: float,threshold: float=.01) -> tuple[float|None,bool]:
    row=db.execute("SELECT value FROM observations WHERE url=? ORDER BY observed_at DESC LIMIT 1",(url,)).fetchone(); previous=row[0] if row else None
    changed=previous is not None and abs(value-previous)/previous >= threshold
    db.execute("INSERT INTO observations VALUES (?,?,?)",(url,value,datetime.now(timezone.utc).isoformat())); db.commit(); return previous,changed
def main():
    p=argparse.ArgumentParser(); p.add_argument("url"); p.add_argument("field"); p.add_argument("--db",type=Path,default=Path("prices.db")); a=p.parse_args(); value=fetch(a.url,a.field); previous,changed=record(connect(a.db),a.url,value); print(f"current={value} previous={previous} alert={changed}")
if __name__=="__main__": main()

