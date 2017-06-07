'''
Analysis class unit test
'''
import sys
sys.path.append('../src/')
import unittest
from data import Data
from account import Account

class AnalysisTest(unittest.TestCase):
    def test_get_suggestion(self):
        # suggestion function test here

if __name__ == '__main__':
    unittest.main()
