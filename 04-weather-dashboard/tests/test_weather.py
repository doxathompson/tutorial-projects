import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from weather import current_weather
class WeatherTests(unittest.TestCase):
    def test_cache_prevents_second_request(self):
        calls=[]
        def fake(url): calls.append(url); return {"current":{"temperature_2m":20}}
        with tempfile.TemporaryDirectory() as raw:
            cache=Path(raw)/"cache.json"; self.assertEqual(current_weather(1,2,cache,fake),current_weather(1,2,cache,fake)); self.assertEqual(len(calls),1)
if __name__=="__main__": unittest.main()

