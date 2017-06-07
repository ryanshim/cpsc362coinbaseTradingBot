'''
Data class unit tests
'''
import sys
sys.path.append('../src/')
import unittest
from account import Account

class DataTest(unittest.TestCase):
    def test_get_spot_price(self):
        # test retrieving current market price

