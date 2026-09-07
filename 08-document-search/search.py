"""Small BM25 search engine for local text documents."""
from __future__ import annotations
import argparse,math,re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
TOKEN=re.compile(r"[a-z0-9]+")
def tokenize(text): return TOKEN.findall(text.lower())
@dataclass
class Document: path:Path; text:str; terms:Counter
def index(root:Path)->list[Document]:
    return [Document(p,(text:=p.read_text(errors="ignore")),Counter(tokenize(text))) for p in root.rglob("*") if p.is_file() and p.suffix in {".txt",".md"}]
def search(documents:list[Document],query:str,limit:int=10):
    if not documents:return []
    avg=sum(sum(d.terms.values()) for d in documents)/len(documents); scores=[]
    for doc in documents:
        score=0.0; length=sum(doc.terms.values())
        for term in tokenize(query):
            frequency=doc.terms[term]; containing=sum(term in d.terms for d in documents)
            idf=math.log(1+(len(documents)-containing+.5)/(containing+.5)); score+=idf*(frequency*2.2)/(frequency+1.2*(.25+.75*length/avg)) if frequency else 0
        if score:scores.append((score,doc))
    return sorted(scores,key=lambda item:item[0],reverse=True)[:limit]
def main():
    p=argparse.ArgumentParser();p.add_argument("directory",type=Path);p.add_argument("query");a=p.parse_args()
    for score,doc in search(index(a.directory),a.query): print(f"{score:.3f} {doc.path}")
if __name__=="__main__":main()

