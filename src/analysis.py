'''
Analysis class:
Performs analysis on historical btc prices to create
a buy/sell sentiment. Uses simple linear regression to
determine trend lines for extrapolated prediction
'''
from sklearn import linear_model
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
#from account import Account
#from data import Data

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

        days = np.reshape(days, (len(days), 1))
        prices = np.reshape(prices, (len(prices), 1))

        regr = linear_model.LinearRegression()

        regr.fit(days, prices)

        data_points = []
        data_points.append(regr.predict(0)[0][0])
        data_points.append(regr.predict(days_index)[0][0])

        if prices_index == 0:   # condition 3 yr
            return self.total_days, self.prices, [0, self.total_days[days_index-2]], data_points
        elif prices_index == 1087:  # condition 1 wk
            return self.total_days[:days_index], self.prices[prices_index:], [0, days_index-1], data_points
        else:
            return self.total_days[:days_index-1], self.prices[prices_index:], [0, days_index-1], data_points
 
if __name__ == '__main__':
    analysis_1 = Analysis()
    scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(1095, 0)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(365, 730)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(184, 911)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(92, 1003)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(31, 1064)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(22, 1073)
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.calc_regression(7, 1087)

    plt.plot(scatter_days, scatter_prices)
    plt.plot(regr_days, regr_prices, ls='--', lw=0.75, color='#9a0000')
    plt.show()





            









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
