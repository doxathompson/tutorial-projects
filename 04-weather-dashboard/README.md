# Weather Dashboard

Fetches Open-Meteo data with no API key and caches it briefly. Dependency
injection keeps network access out of unit tests.

```bash
python weather.py -18.8792 47.5079
python -m unittest discover -s tests -v
```

