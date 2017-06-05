'''
Account class unit tests
'''
import unittest
from account import Account

class AccountTest(unittest.TestCase):

    def test_get_acct_name(self):
        acct = Account()
        self.assertEqual(acct.get_acct_name(), 'My Wallet')

    def test_get_acct_id(self):
        acct = Account()
        self.assertEqual(acct.get_acct_id(), '7e1e86df-0b3a-59b7-ab78-a898a0800185')

    def test_get_acct_balance(self):
        acct = Account()
        self.assertEqual(acct.get_acct_balance(), ('0.02252686', 'BTC'))

if __name__ == '__main__':
    unittest.main()
