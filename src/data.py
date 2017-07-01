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
    get most recent buy price
    '''
    def get_buy_price(self):
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + "prices/BTC-USD/buy", auth=auth)
        output = dict(req.json())
        return output['data']['amount']


    '''
    get most recent sell price
    '''
    def get_sell_price(self):
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + "prices/BTC-USD/sell", auth=auth)
        output = dict(req.json())
        return output['data']['amount']


    '''
    get prices helper function
    '''
    def get_prices_helper(self, lst_times):
        prices = []
        auth = CoinbaseWalletAuth()

        for time in lst_times:
            try:
                req = requests.get(self.api_url + 'prices/BTC-USD/spot',
                                   'date=' + str(time), auth=auth)
                output = dict(req.json())
                spot_amt = output['data']['amount']
                spot_currency = output['data']['currency']
                prices.append([spot_amt, spot_currency])
            except RuntimeError:
                print("Price data for: " + str(time) + " failed to retrieve\n")

        return prices


    '''
    get historical prices of beg each month
    from the last 6 months
    '''
    def get_6_month_prices(self):
        time_points = []
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

        prices = self.get_prices_helper(time_points)

        return prices


    '''
    get historical prices of 
    past 4 weeks
    '''
    def get_4_week_prices(self):
        time_points = []

        # get time points of beg of each week
        for i in range(1,5):
            time_points.append(dt.date.today() - dt.timedelta(weeks=i))

        prices = self.get_prices_helper(time_points)

        return prices


    '''
    get historical prices of beg
    of last 7 days
    '''
    def get_7_day_prices(self):
        time_points = []

        # get time points
        for i in range(1,8):
            time_points.append(dt.date.today() - dt.timedelta(days=i))

        prices = self.get_prices_helper(time_points)

        return prices


    '''
    get prices of the past 3 years
    '''
    def get_3yr_daily_price(self):
        if self.is_update():
            # calc num of days past since last update
            curr_date = dt.datetime.today().date()
            days_delta = self.get_diff_days()

            # retrieve existing price data
            with open('prices.txt', 'r') as infile:
                infile.readline() # skip over the last updated line
                prices = infile.readlines()
            
            # write new price data
            outfile = open('prices.txt', 'w')
            outfile.write(str(curr_date) + "\n")

            # add the missing days between updates
            for i in range(1, days_delta+1):
                #print("Retrieving day minus " + str(i))
                time_point = dt.date.today() - dt.timedelta(days=i)

                # api call
                try:
                    auth = CoinbaseWalletAuth()
                    req = requests.get(self.api_url + "prices/BTC-USD/spot",
                                       "date=" + str(time_point), auth=auth)
                except RuntimeError:
                    print("Could not retrieve price for today minus " + str(i))

                output = dict(req.json())
                spot_amt = output['data']['amount']

                outfile.write(str(time_point) + "\t" + spot_amt + "\n")

            # write the remaining days that do not
            # need to be updated
            for line in prices[:1094-days_delta]:
                outfile.write(line)

            outfile.close() 
            print("New prices saved")
            return days_delta
        else:
            print("No update required")
            return 0


    '''
    Check last update condition
    '''
    def is_update(self):
        curr_date = dt.datetime.today().date()
        with open('prices.txt', 'r') as infile:
            last_update = infile.readline()
        if (str(curr_date) + "\n") != last_update:
            return True
        else:
            return False


    '''
    Get num days from last update
    '''
    def get_diff_days(self):
        curr_date = dt.datetime.today().date()
        with open('prices.txt', 'r') as infile:
            last_update_date = infile.readline().strip("\n")
            last_update = dt.datetime.strptime(last_update_date, "%Y-%m-%d")
            days_delta = (curr_date - last_update.date()).days
        return days_delta


    '''
    Parse price data from txt file
    '''
    def parse_prices_file(self, num_days):
        infile = open('prices.txt', 'r')

        lst_prices = []
        lst_dates = []

        last_update = infile.readline()

        for i in range(1,1095):
            line = infile.readline().split("\t")
            line[1] = line[1].strip("\n")
            lst_prices.append(line[1])
            lst_dates.append(dt.datetime.strptime(line[0], "%Y-%m-%d"))

        infile.close()

        return lst_prices, lst_dates


    '''
    get the exchange ranges available on CB
    '''
    def get_exchange_rates(self):
        auth = CoinbaseWalletAuth()
        req = requests.get(self.api_url + 'exchange-rates',
                           params='currency=BTC',
                           auth=auth).json()
        output = dict(req['data']['rates'])
        return output

    '''
    convert currency (BTC -> OTHER)
    '''
    def convert_currency_btc(self, amount, code):
        rates = self.get_exchange_rates()
        return float(amount) * float(rates[code])


    '''
    convert currency (OTHER -> BTC)
    '''
    def convert_currency_oth(self, amount, code):
        rates = self.get_exchange_rates()
        return float(amount) / float(rates[code])

