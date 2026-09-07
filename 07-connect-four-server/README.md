# Connect Four Server

A thread-per-connection TCP server. Send a column number (`0`–`6`) per line.
The core game is independent of networking and fully testable.

```bash
python server.py
python -m unittest discover -s tests -v
```

