'''
Data class
Retrieves misc. data from the CB API
'''
import json
import requests
import datetime as dt
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

    '''
    current market btc price
    '''
    def get_spot_price(self):
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + 'prices/BTC-USD/spot', auth=auth)
        output = dict(req.json())

        self.spot_price_amt = output['data']['amount']
        self.spot_price_currency = output['data']['currency']

        return [self.spot_price_amt, self.spot_price_currency]

    '''
    get historical prices of beg each month
    from the last 6 months
    '''
    def get_6_month_prices(self):
        time_points = []
        prices = []
        date = dt.date.today()

        # create timestamps
        for i in range(-6,0):
            m = (date.month + i) % 12   # determine month
            if m is 0:
                m = 12

            y = date.year + ((date.month) + i - 1) // 12 # determine year

            # find days
            if (y % 4 == 0) and not (y % 400 == 0): # determine if leap year
                feb_days = 29
            else:
                feb_days = 28
            days_in_months = [31, feb_days, 31, 30, 31, 30,
                              31, 31, 30, 31, 30, 31][m-1]

            d = min(date.day, days_in_months)

            time_points.append(date.replace(day=d, month=m, year=y))

        # initiate API call
        auth = CoinbaseWalletAuth()

        for j in time_points:
            req = requests.get(self.api_url + 'prices/BTC-USD/spot',
                               'date=' + str(time_points[j]), auth=auth)
            output = dict(req.json())
            spot_amt = output['data']['amount']
            spot_currency = output['data']['currency']
            prices.append([spot_amt, spot_currency])

        return prices

    '''
    get historical prices of 
    past 4 weeks
    '''
    def get_4_week_prices(self):
        time_points = []
        prices = []

        # get time points of beg of each week
        for i in range(1,5):
            time_points.append(dt.date.today() - dt.timedelta(weeks=i))

            # initiate API call
            req = requests.get(self.api_url + 'prices/BTC-USD/spot',
                               'date=' + time_points[j], auth=auth)
            output = dict(req.json())
            spot_amt = output['data']['amount']
            spot_currency = output['data']['currency']
            prices.append[[spot_amt, spot_currency]]

        return prices

    '''
    get historical prices of beg
    of last 7 days
    '''
    def get_7_day_prices(self):
        time_points = []
        prices = []

        # get time points
        for i in range(1,8):
            time_points.append(dt.date.today() - dt.timedelta(days=i))

        # initiate API call
        auth = CoinbaseWalletAuth()

        for j in time_points:
            req = requests.get(self.api_url + 'prices/BTC-USD/spot',
                               'date=' + time_points[j], auth=auth)
            output = dict(req.json())
            spot_amt = output['data']['amount']
            spot_currency = output['data']['currency']
            prices.append[[spot_amt, spot_currency]]

        return prices

    '''
    get the exchange ranges for the
    top 5 most used currencies
    '''
    def get_exchange_rates(self, convert_amt):
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + 'exchange-rates', auth=auth).json()
        output = dict(req['data']['rates'])

        exchange_list = []
        for k,v in output.iteritems():
            if (key == 'BTC'):
                exchange_list.append("%.6f" % (float(convert)*float(value)))
                exchange_list.append(key)
            if ((key == 'USD') or (key == 'EUR') or (key == 'JPY') or (key == 'GBP') or (key == 'CHF')):
                exchange_list.append("%.2f" % (float(convert)*float(value)))
                exchange_list.append(key)

        return exchange_list

