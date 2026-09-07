import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from search import index,search
class SearchTests(unittest.TestCase):
    def test_relevant_document_ranks_first(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw);(root/"python.md").write_text("python python testing");(root/"cooking.txt").write_text("bread recipe")
            self.assertEqual(search(index(root),"python")[0][1].path.name,"python.md")
if __name__=="__main__":unittest.main()
