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

    def test_get_price_hist_6_mon(self):
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_6_mon(), '')

    def test_get_price_hist_cur_mon(self):
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_mon(), '')

    def test_get_price_hist_cur_wk(self):
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_wk(), '')

    def test_get_price_hist_cur_hr(self):
        data_1 = Data()
        self.assertEqual(data_1.get_price_hist_cur_hr(), '')

    def test_get_exchange_rates(self):
        data_1 = Data()
        self.assertEqual(data_1.get_exchange_rates(), '')

if __name__ == '__main__':
    unittest.main()
