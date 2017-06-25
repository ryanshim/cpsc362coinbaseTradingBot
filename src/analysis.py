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

    def regr_three_yr(self):
        days = self.total_days
        prices = self.prices

        days = np.reshape(days, (len(days), 1))
        prices = np.reshape(prices, (len(prices), 1))

        regr = linear_model.LinearRegression()

        regr.fit(days, prices)

        data_points = []
        data_points.append(regr.predict(0)[0][0])
        data_points.append(regr.predict(1095)[0][0])

        return self.total_days, self.prices, [0, self.total_days[1093]], data_points

    def regr_one_yr(self):
        days = self.total_days[:365]
        prices = self.prices[729:]
        print(len(prices))

        days = np.reshape(days, (len(days), 1))
        prices = np.reshape(prices, (len(prices), 1))

        regr = linear_model.LinearRegression()

        regr.fit(days, prices)

        data_points = []
        data_points.append(regr.predict(0)[0][0])
        data_points.append(regr.predict(365)[0][0])

        return self.total_days[:364], self.prices[730:], [0, 364], data_points


if __name__ == '__main__':
    analysis_1 = Analysis()
    scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.regr_three_yr()
    #scatter_days, scatter_prices, regr_days, regr_prices = analysis_1.regr_one_yr() 


    plt.scatter(scatter_days, scatter_prices, s=1)
    plt.plot(regr_days, regr_prices, ls='--', color='#9a0000')
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
