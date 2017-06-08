'''
Data class
Retrieves misc. data from the CB API
'''
import json
import requests
from coinbasewalletauth import CoinbaseWalletAuth

class Data():
    def __init__(self):
        # initialize generic api url
        self.api_url = "https://api.coinbase.com/v2/"

        # initial setup
        auth = CoinbaseWalletAuth()

        # member variables
        self.spot_price_amt = 0
        self.spot_price_currency = ''

    # current market btc price
    def get_spot_price():
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + 'prices/BTC-USD/spot', auth=auth)
        output = dict(req.json())

        self.spot_price_amt = output['data']['amount']
        self.spot_price_currency = output['data']['currency']

        return [self.spot_price_amt, self.spot_price_currency]

    # get historical prices of beg each month
    # from the last 6 months
    def get_price_hist_6_mon():
        return

    # get historical prices of beg of each week
    # from the current month
    def get_price_hist_cur_mon():
        return

    # get historical prices of beg of each day
    # from the current week
    def get_price_hist_cur_wk():
        return

    # get historical prices of each hour
    # from current day to the current hour
    def get_price_hist_cur_hr():
        return
