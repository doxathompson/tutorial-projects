import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from assistant import answer,ingest,retrieve
class AssistantTests(unittest.TestCase):
    def test_answer_contains_real_citation(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);(root/"guide.md").write_text("Automated tests catch regressions. They also document expected behavior.")
            result=answer("Why use automated tests?",ingest(root));self.assertIn("[guide.md#p1]",result);self.assertIn("tests",result)
    def test_unknown_topic_is_honest(self):self.assertIn("could not find",answer("anything",[]))
if __name__=="__main__":unittest.main()
