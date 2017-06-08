'''
Data class unit tests
'''
import sys
sys.path.append('../src/')
import unittest
from data import Data

class DataTest(unittest.TestCase):
    def test_get_spot_price(self):
        data_1 = Data()
        self.assertEqual('data_1.get_spot_price()', 'data_1.get_spot_price()')

    def test_get_price_hist_6_mon():
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_6_mon(), '')

    def test_get_price_hist_cur_mon():
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_mon(), '')

    def test_get_price_hist_cur_wk():
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_wk(), '')

    def test_get_price_hist_cur_hr():
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_hr(), '')

if __name__ == '__main__':
    unittest.main()
