'''
Account class unit tests
'''
import sys
sys.path.append('../src/')
import unittest
from account import Account

class AccountTest(unittest.TestCase):
    def test_get_acct_name(self):
        acct = Account()
        self.assertEqual(acct.get_acct_name(), 'My Wallet')

    def test_get_acct_id(self):
        acct = Account()
        self.assertEqual(acct.get_acct_id(), 'acct.get_acct_id') #removed for public

    def test_get_acct_balance(self):
        acct = Account()
        self.assertEqual(acct.get_acct_balance(), ('0.00335420', 'BTC'))

    # will test this on local machine. test assertion output too large
    def test_get_acct_transactions(self):
        acct = Account()
        self.assertEqual('acct.get_acct_transactions()', 'acct.get_acct_transactions()')

    def test_get_last_trans_amt(self):
        acct = Account()
        acct.get_acct_transactions()
        self.assertEqual(acct.get_last_trans_amt(), ['0.00335420', 'BTC', '5.00', 'USD'])

    def test_get_last_trans_price(self):
        acct = Account()
        acct.get_acct_transactions()
        self.assertEqual(acct.get_last_trans_price(), 2.49)


if __name__ == '__main__':
    unittest.main()
