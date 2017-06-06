'''
Account class: any member variables and functions related to a
bitcoin account will go here
'''
import json
import requests
from coinbasewalletauth import CoinbaseWalletAuth

class Account():
    def __init__(self):
        # initialize generic api url
        self.api_url = "https://api.coinbase.com/v2/"

        # initial setup
        auth = CoinbaseWalletAuth() 

    def get_acct_name(self):
        # add acct name function here
        return

    def get_acct_id(self):
        # add acct id function here
        return

    def get_acct_balance(self):
        # get current balance in this form (balance, currency_type)
        # the variables in the tuple above are string types
        return

    def get_acct_transactions(self):
        # add function to get list of transactions here
        return

    def get_last_transaction_price(self):
        # add function to get last transaction price here
        return
