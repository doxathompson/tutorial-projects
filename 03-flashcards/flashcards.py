"""A compact flashcard CLI with spaced-repetition scheduling."""
from __future__ import annotations
import argparse, json
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path

@dataclass(frozen=True)
class Card:
    question: str
    answer: str
    due: str
    interval: int = 0
    ease: float = 2.5
    repetitions: int = 0

def review(card: Card, quality: int, today: date | None = None) -> Card:
    """Return new state; immutable inputs make review rules easy to test."""
    if quality not in range(6): raise ValueError("quality must be 0..5")
    today = today or date.today()
    reps = card.repetitions + 1 if quality >= 3 else 0
    interval = 1 if reps == 1 else 6 if reps == 2 else round(card.interval * card.ease)
    if quality < 3: interval = 1
    ease = max(1.3, card.ease + (0.1 - (5-quality)*(0.08+(5-quality)*0.02)))
    return Card(card.question, card.answer, (today + timedelta(days=interval)).isoformat(), interval, ease, reps)

def load(path: Path) -> list[Card]:
    return [Card(**row) for row in json.loads(path.read_text())] if path.exists() else []

def save(path: Path, cards: list[Card]) -> None:
    path.write_text(json.dumps([asdict(c) for c in cards], indent=2)+"\n")

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--file",type=Path,default=Path("cards.json"))
    sub=parser.add_subparsers(dest="cmd",required=True); add=sub.add_parser("add"); add.add_argument("question"); add.add_argument("answer"); sub.add_parser("study")
    args=parser.parse_args(); cards=load(args.file)
    if args.cmd=="add": cards.append(Card(args.question,args.answer,date.today().isoformat())); save(args.file,cards); return
    for index, card in enumerate(cards):
        if card.due > date.today().isoformat(): continue
        print(card.question); input("Press Enter to reveal: "); print(card.answer)
        quality=int(input("Recall quality (0-5): ")); cards[index]=review(card,quality)
    save(args.file,cards)
if __name__=="__main__": main()

