# Price-Change Tracker

Separates fetching, persistence, and alert policy. The demo tracks a JSON API
field; use only APIs/sites whose terms allow automation.

```bash
python tracker.py URL price --db prices.db
python -m unittest discover -s tests -v
```

