"""Weather client showing HTTP boundaries, timeouts, and TTL caching."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from typing import Callable
from urllib.parse import urlencode
from urllib.request import urlopen

def fetch_json(url: str) -> dict:
    # Every network call needs a timeout; hanging forever is not a strategy.
    with urlopen(url,timeout=10) as response: return json.load(response)

def current_weather(lat: float, lon: float, cache: Path, get: Callable[[str],dict]=fetch_json, ttl: int=600) -> dict:
    if cache.exists() and time.time()-cache.stat().st_mtime < ttl: return json.loads(cache.read_text())
    query=urlencode({"latitude":lat,"longitude":lon,"current":"temperature_2m,wind_speed_10m","timezone":"auto"})
    data=get("https://api.open-meteo.com/v1/forecast?"+query)
    cache.write_text(json.dumps(data)); return data

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("latitude",type=float); p.add_argument("longitude",type=float); p.add_argument("--cache",type=Path,default=Path("weather-cache.json")); a=p.parse_args()
    current=current_weather(a.latitude,a.longitude,a.cache)["current"]
    print(f"{current['temperature_2m']}°C, wind {current['wind_speed_10m']} km/h")
if __name__=="__main__": main()

