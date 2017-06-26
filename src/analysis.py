'''
Analysis class:
Performs analysis on historical btc prices to create
a buy/sell sentiment. Uses simple linear regression to
determine trend lines for extrapolated prediction
'''
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
#from account import Account
from data import Data

class Analysis:
    def __init__(self):
        self.total_days = [x for x in range(1094)]
        self.prices = []

        with open('prices.txt', 'r') as infile:
            infile.readline()
            data = infile.readlines()
            for x in data:
                line = x.split('\t')
                self.prices.append(float(line[1].strip('\n')))

        self.prices.reverse()

    '''
    Perform linear regression on the range of time inputs.
    First two return var's are used to plot the actual data
    and the last two are to plot the linear regression line
    '''
    def calc_regression(self, days_index, prices_index):
        if prices_index == 0:   # condition for 3 yr
            days = self.total_days
            prices = self.prices
        elif prices_index == 1087:  # condition for 1 wk
            days = self.total_days[:days_index]
            prices = self.prices[prices_index:]
        else:
            days = self.total_days[:days_index]
            prices = self.prices[prices_index-1:]

        # reshape days and price lists to nx1 matrix 
        days = np.reshape(days, (len(days), 1)) 
        prices = np.reshape(prices, (len(prices), 1))

        # instantiate lin reg object
        regr = linear_model.LinearRegression()

        # fit data into linear model
        regr.fit(days, prices)

        # predict prices for beg and end
        data_points = []
        data_points.append(regr.predict(0)[0][0])
        data_points.append(regr.predict(days_index)[0][0])

        if prices_index == 0:   # condition 3 yr
            return self.total_days, self.prices, [0, self.total_days[days_index-2]], data_points
        elif prices_index == 1087:  # condition 1 wk
            return self.total_days[:days_index], self.prices[prices_index:], [0, days_index-1], data_points
        else:
            return self.total_days[:days_index-1], self.prices[prices_index:], [0, days_index-1], data_points


    ''' get 24 hr percent change '''
    def calc_one_dy_change(self, cls_data):
        week_prices = cls_data.get_7_day_prices()
        previous_day = float(week_prices[1][0])
        return self.calc_perc_delta(previous_day, cls_data)

    ''' get % delta since last week '''
    def calc_one_wk_change(self, cls_data):
        week_prices = cls_data.get_7_day_prices()
        previous_week = float(week_prices[6][0])
        return self.calc_perc_delta(previous_week, cls_data)

    ''' get % delta since last 3 weeks '''
    def calc_three_wk_change(self, cls_data):
        three_wk_prices = cls_data.get_4_week_prices()
        three_wk = float(three_wk_prices[2][0])
        return self.calc_perc_delta(three_wk, cls_data)

    ''' get % delta since last month '''
    def calc_one_mn_change(self, cls_data):
        one_mon_prices = cls_data.get_4_week_prices()
        one_mon = float(one_mon_prices[3][0])
        return self.calc_perc_delta(one_mon, cls_data)

    ''' get % delta since last 3 months '''
    def calc_three_mn_change(self, cls_data):
        three_mon_prices = cls_data.get_6_month_prices()
        three_mon = float(three_mon_prices[2][0])
        return self.calc_perc_delta(three_mon, cls_data)

    ''' get % delta since last 6 months '''
    def calc_six_mn_change(self, cls_data):
        six_mon_prices = cls_data.get_6_month_prices()
        six_mon = float(six_mon_prices[5][0])
        return self.calc_perc_delta(six_mon, cls_data)

    '''
    Calculate the percentage change from the input price
    and the current spot price
    '''
    def calc_perc_delta(self, old, cls_data):
        spot_price = cls_data.get_spot_price()
        perc_change = ((float(spot_price[0]) - old) / old) * 100
        return perc_change

 
'''
if __name__ == '__main__':
    analysis_1 = Analysis()
    data_1 = Data()
    print(data_1.get_4_week_prices())

    # 3 yr
    scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(1095, 0)
    # 1 yr
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(365, 730)
    # 6 mon
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(184, 911)
    # 3 mon
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(92, 1003)
    # 1 mon
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(31, 1064)
    # 3 wk
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(22, 1073)
    # 1 wk
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(7, 1087)

    plt.plot(scatter_days, scatter_prices)
    plt.plot(regr_days, regr_prices, ls='--', lw=0.75, color='#9a0000')
    plt.show()
'''





            









'''
def main():
    infile = open('prices.txt', 'r')
    last_update = infile.readline()   # skip over the first line
    data = infile.readlines()   # read the data

    # create a list of training data
    days = []
    prices = []
    day = 1093
    for x in data:
        line = x.split('\t')
        days.append(day)
        prices.append(float(line[1].strip('\n')))
        day -= 1

    days.reverse()
    prices.reverse()

    plt.scatter(days, prices, s=1)

    regr = linear_model.LinearRegression()
    days = np.reshape(days, (len(days), 1))
    prices = np.reshape(prices, (len(prices), 1))
    
    regr.fit(days, prices)
    predicted_price = regr.predict(1458)
    print(regr.coef_)
    print(regr.intercept_)
    print(predicted_price)


    data_points = []
    data_points.append(regr.intercept_)
    data_points.append((regr.intercept_ + regr.coef_*len(days)))


    
    days_plot = [0, len(days)]

        
    plt.plot(days_plot, data_points, ls='--', color='#0de521')
    plt.show()


if __name__ == '__main__':
    main()
'''
