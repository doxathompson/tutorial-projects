import sys,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from api import hash_password,token_for,user_from_token,verify_password
class SecurityTests(unittest.TestCase):
    def test_password_round_trip(self):
        stored=hash_password("correct horse battery");self.assertTrue(verify_password("correct horse battery",stored));self.assertFalse(verify_password("wrong password",stored))
    def test_signed_token(self):self.assertEqual(user_from_token(token_for(42)),42)
    def test_expired_token(self):
        with self.assertRaises(PermissionError):user_from_token(token_for(1,int(time.time())-1))
if __name__=="__main__":unittest.main()

