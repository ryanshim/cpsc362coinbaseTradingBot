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

    # current market btc price
    def get_spot_price():
        return

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
    def get_price_hist_cur_week():
        return

    # get historical prices of each hour
    # from current day to the current hour
    def get_price_hist_cur_hour():
        return
