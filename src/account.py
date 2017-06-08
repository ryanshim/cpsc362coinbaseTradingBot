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
        self.acct_last_trans_amt = []
        self.acct_last_trans_price = 0

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
        account_id = self.get_acct_id()
        auth = CoinbaseWalletAuth()
        request_transaction = requests.get(self.api_url + \
                                           'accounts/' + \
                                           account_id + \
                                           '/transactions', auth=auth).json()
        output = dict(request_transaction)

        i = 0
        trans_list = []
        for i in range(5):
            trans_list.append(output['data'][i])

        self.acct_last_trans_price.append(output['data'][0]['amount']['amount'])
        self.acct_last_trans_price.append(output['data'][0]['amount']['currency'])
        self.acct_last_trans_price.append(output['data'][0]['native_amount']['amount'])
        self.acct_last_trans_price.append(output['data'][0]['native_amount']['currency'])

        return trans_list

    # returns a list containing 2 k,v pairs for amount and native amt as keys
    def get_last_trans_amt(self):
        return self.acct_last_trans_amt

    def get_last_trans_price(self):
        return self.acct_last_trans_price

