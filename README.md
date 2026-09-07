# Python Project Ladder

Ten progressively harder, portfolio-ready Python projects. Each directory is an
independent project with its own README, implementation, and tests.

| # | Project | Main ideas |
|---|---|---|
| 01 | Expense Tracker | CLI design, JSON persistence, money handling |
| 02 | File Organizer | Filesystems, hashing, safe automation |
| 03 | Flashcards | Domain modelling, spaced repetition |
| 04 | Weather Dashboard | HTTP APIs, caching, dependency boundaries |
| 05 | Finance Web App | Web apps, SQLite, service layers |
| 06 | Price Tracker | Scheduling, change detection, notifications |
| 07 | Connect Four Server | Networking, concurrency, game state |
| 08 | Document Search | Indexing, ranking, text processing |
| 09 | Production Task API | Authentication, migrations, observability |
| 10 | Research Assistant | Retrieval, citations, evaluation |

Start at `01-expense-tracker` and read its README before the code. A useful way
to study the repository is to inspect each milestone with `git log --oneline`
and `git show <commit>`.

## Engineering conventions

- Python 3.11+ and type hints throughout.
- Standard-library-first, with third-party dependencies added only when useful.
- Tests use `unittest`, so most projects can be tested without extra tooling.
- Public functions explain *why* they exist; inline comments explain decisions,
  not obvious syntax.
- External services sit behind small interfaces so business logic stays easy to
  test.

