# File Organizer and Duplicate Finder

Safely plans file moves by extension and finds byte-for-byte duplicates. The
default `plan` command changes nothing; `apply` must be explicit.

```bash
python organizer.py plan ~/Downloads
python organizer.py apply ~/Downloads
python organizer.py duplicates ~/Downloads
python -m unittest discover -s tests -v
```

The two-phase plan/apply design is common in production migration tools: users
can inspect risky operations before allowing mutation.

