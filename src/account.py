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

        # initial setup on instantiation
        auth = CoinbaseWalletAuth() # call authentication class
        req = requests.get(self.api_url + 'accounts', auth=auth)
        output = dict(req.json())


        # initial setup
        self.acct_id = output['data'][0]['id'] 
        self.acct_name = output['data'][0]['name']
        self.acct_balance = 0

        # this is where member variables will go

    # retrieve account name
    def get_acct_name(self):
        return self.acct_name

    # add acct id function here
    def get_acct_id(self):
        return self.acct_id

    def get_acct_balance(self):
        # get current balance in this form (balance, currency_type)
        # the variables in the tuple above are string types
        auth = CoinbaseWalletAuth()

        req = requests.get(self.api_url + 'accounts', auth=auth)
        output = dict(req.json())

        curr_amount = output['data'][0]['balance']['amount']
        curr_type = output['data'][0]['balance']['currency']

        self.acct_balance = curr_amount

        return self.acct_balance, curr_type

    def get_acct_transactions(self):
        # add function to get list of transactions here
        return

    def get_last_transaction_price(self):
        # add function to get last transaction price here
        return
