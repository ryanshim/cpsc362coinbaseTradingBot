'''
Data class unit tests
'''
import sys
sys.path.append('../src/')
import unittest
from data import Data

class DataTest(unittest.TestCase):

    # this next test should output 0 since there 
    # is no update required
    def test_get_3yr_daily_price(self):
        data_1 = Data()
        self.assertEqual(data_1.get_3yr_daily_price(), 0)

    # this test should output the date of the last
    # update in the first line of the file
    def test_last_update(self):
        with open('prices.txt', 'r') as infile:
            last_update = infile.readline()
        self.assertEqual(last_update, "2017-06-30\n")


if __name__ == '__main__':
    unittest.main()
