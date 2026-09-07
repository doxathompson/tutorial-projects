import sys, unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from flashcards import Card, review
class ReviewTests(unittest.TestCase):
    def test_success_schedules_tomorrow(self):
        card=Card("Q","A","2026-01-01")
        result=review(card,5,date(2026,1,1)); self.assertEqual(result.due,"2026-01-02"); self.assertEqual(result.repetitions,1)
    def test_failure_resets_progress(self):
        card=Card("Q","A","2026-01-01",10,2.5,4)
        result=review(card,1,date(2026,1,1)); self.assertEqual((result.interval,result.repetitions),(1,0))
if __name__=="__main__": unittest.main()

