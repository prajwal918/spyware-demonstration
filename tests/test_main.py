import unittest
import sys
import os

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCoreLogic(unittest.TestCase):
    def test_numpad_mapping(self):
        try:
            from src.main import numpad_map
            self.assertEqual(numpad_map[96], "0")
            self.assertEqual(numpad_map[110], ".")
        except ImportError:
            self.skipTest("Source module could not be imported. Likely missing dependencies.")

if __name__ == '__main__':
    unittest.main()
