"""Local research assistant that makes every answer traceable to source text."""
from __future__ import annotations
import argparse,math,re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
TOKEN=re.compile(r"[a-z0-9]+")
SENTENCE=re.compile(r"(?<=[.!?])\s+")
def terms(text:str):return TOKEN.findall(text.lower())
@dataclass(frozen=True)
class Passage:
    source:Path;number:int;text:str
    @property
    def citation(self):return f"{self.source.name}#p{self.number}"
def ingest(root:Path,words_per_passage:int=120)->list[Passage]:
    passages=[]
    for source in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in {".txt",".md"}):
        words=source.read_text(errors="ignore").split()
        for offset in range(0,len(words),words_per_passage):passages.append(Passage(source,offset//words_per_passage+1," ".join(words[offset:offset+words_per_passage])))
    return passages
def retrieve(passages:list[Passage],question:str,limit:int=3)->list[Passage]:
    query=set(terms(question));doc_terms=[Counter(terms(p.text)) for p in passages];scores=[]
    for passage,counts in zip(passages,doc_terms):
        score=sum((1+math.log(counts[t]))*math.log(1+len(passages)/(1+sum(t in d for d in doc_terms))) for t in query if counts[t])
        if score:scores.append((score,passage))
    return [p for _,p in sorted(scores,key=lambda x:x[0],reverse=True)[:limit]]
def answer(question:str,passages:list[Passage])->str:
    selected=retrieve(passages,question)
    if not selected:return "I could not find relevant evidence in the provided documents."
    query=set(terms(question));lines=[]
    for passage in selected:
        # Extracting the most overlapping sentence avoids inventing unsupported facts.
        sentence=max(SENTENCE.split(passage.text),key=lambda s:len(query & set(terms(s))))
        lines.append(f"{sentence.strip()} [{passage.citation}]")
    return "\n".join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument("directory",type=Path);p.add_argument("question");a=p.parse_args();print(answer(a.question,ingest(a.directory)))
if __name__=="__main__":main()

