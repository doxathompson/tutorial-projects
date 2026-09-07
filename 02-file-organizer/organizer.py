"""Previewable file organization with collision and duplicate protection."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "documents": {".pdf", ".txt", ".md", ".docx"},
    "archives": {".zip", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".html", ".css"},
}


@dataclass(frozen=True)
class Move:
    source: Path
    destination: Path


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    return next((name for name, suffixes in CATEGORIES.items() if suffix in suffixes), "other")


def plan_moves(directory: Path) -> list[Move]:
    moves: list[Move] = []
    reserved: set[Path] = set()
    for source in sorted(path for path in directory.iterdir() if path.is_file()):
        destination = directory / category_for(source) / source.name
        counter = 1
        # Never overwrite. The reserved set also handles two planned files that
        # would resolve to the same destination before anything has moved.
        while destination.exists() or destination in reserved:
            destination = destination.with_stem(f"{source.stem}-{counter}")
            counter += 1
        reserved.add(destination)
        moves.append(Move(source, destination))
    return moves


def apply_moves(moves: list[Move]) -> None:
    for move in moves:
        move.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(move.source, move.destination)


def file_digest(path: Path, chunk_size: int = 64 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(directory: Path) -> list[list[Path]]:
    # Grouping by size first avoids hashing files that cannot possibly match.
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in directory.rglob("*"):
        if path.is_file():
            by_size[path.stat().st_size].append(path)
    groups: list[list[Path]] = []
    for candidates in by_size.values():
        if len(candidates) < 2:
            continue
        by_hash: dict[str, list[Path]] = defaultdict(list)
        for path in candidates:
            by_hash[file_digest(path)].append(path)
        groups.extend(paths for paths in by_hash.values() if len(paths) > 1)
    return groups


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("plan", "apply", "duplicates"))
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error("directory does not exist")
    if args.command == "duplicates":
        for group in find_duplicates(args.directory):
            print("duplicate group:")
            print(*(f"  {path}" for path in group), sep="\n")
    else:
        moves = plan_moves(args.directory)
        for move in moves:
            print(f"{move.source.name} -> {move.destination.relative_to(args.directory)}")
        if args.command == "apply":
            apply_moves(moves)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

