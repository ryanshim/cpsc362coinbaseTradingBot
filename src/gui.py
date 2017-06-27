'''
Gui class created with Tkinter
'''
# thread related imports
import _thread
import time
import datetime as dt

# gui module imports
import tkinter as tk
from tkinter import ttk

# matplot lib imports
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg 

# backend class imports
from account import Account
from analysis import Analysis
from data import Data

# gui globals
LARGE_FONT = ("Free Sans", 12)
HEADER_FONT = ("Free Sans", 10, 'bold')
WIN_LENGTH = 1000 
WIN_WIDTH = 600
BG_COLOR = "#FFFFFF"
FG_COLOR = "#303642"
INC_COLOR = "#005D12"
DEC_COLOR = "#AB0000"


class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "CB Trading Bot")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)    # 0 is min size
                                                    # weight is priority (just use 1)
        container.grid_columnconfigure(0, weight=1)

        # MENU BAR CONFIG
        menu_bar = tk.Menu(container)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="CB Account",
                              command=lambda: self.show_frame(Account_Page))
        file_menu.add_separator()

        file_menu.add_command(label="BTC Data",
                              command=lambda: self.show_frame(Data_Page))
        file_menu.add_separator()

        file_menu.add_command(label="BTC Analysis",
                              command=lambda: self.show_frame(Analysis_Page))
        file_menu.add_separator()

        file_menu.add_command(label="Main Page",
                              command=lambda: self.show_frame(Main_Page))

        file_menu.add_command(label="Exit", command=quit)

        menu_bar.add_cascade(label="File", menu=file_menu)

        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}

        for fm in (Main_Page, Account_Page, Data_Page, Analysis_Page):
            frame = fm(container, self)
            self.frames[fm] = frame
            frame.grid(row=0, column=0, sticky='nsew')  # sticky (stretch win items north
                                                        # south east west)

        self.show_frame(Main_Page)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()





'''
Main Opening Window
'''
class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Coinbase Trading Application",
                         font=LARGE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        label.place(x=400, y=30)

        # retrieve daily btc prices for
        # past 3 years
        days_delta = data.get_3yr_daily_price()
        lst_prices, lst_dates = data.parse_prices_file(days_delta)

        # insert an overview of prices of btc
        # for past 3 years
        f = matplotlib.figure.Figure(figsize=(8,5), dpi=100, facecolor=BG_COLOR)
        a = f.add_subplot(111, ylabel="USD", facecolor=BG_COLOR)

        plot_title = "BTC Prices"
        a.set_title(plot_title, color=FG_COLOR)

        a.spines['top'].set_color(FG_COLOR)
        a.spines['bottom'].set_color(FG_COLOR)
        a.spines['left'].set_color(FG_COLOR)
        a.spines['right'].set_color(FG_COLOR)
        a.tick_params(axis='x', colors=FG_COLOR)
        a.tick_params(axis='y', colors=FG_COLOR)
        a.yaxis.label.set_color(FG_COLOR)
        a.xaxis.label.set_color(FG_COLOR)

        a.plot(lst_dates, lst_prices)
        labels = a.get_xticklabels()
        plt.setp(labels, rotation=30)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x=100, y=60)

        '''
        # matplotlib toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x=(WIN_LENGTH // 10), y=80)
        '''
        # display last spot price
        price_lbl = tk.Label(self, text="Last BTC price: ", bg=BG_COLOR, fg=FG_COLOR)
        price_lbl.place(x=410, y=65)
        self.start_threads_main()


    def start_threads_main(self):
        _thread.start_new_thread(self.retrieve_spot_price, (data, 30))

    def retrieve_spot_price(self, cls_data, delay):
        try:
            while 1:
                spot_price = cls_data.get_spot_price()
                spot_price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                          text=spot_price[0] + " " + spot_price[1])
                spot_price_lbl.place(x=510, y=65)
                time.sleep(delay)
        except RuntimeError:
            print("Failed to load spot price")
            print("Trying again...")
            while 1:
                spot_price = cls_data.get_spot_price()
                spot_price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                          text=spot_price[0] + " " + spot_price[1])
                spot_price_lbl.place(x=510, y=65)
                time.sleep(delay)



'''
Account information page
'''
class Account_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        # Page title
        pg_title = tk.Label(self, text="Coinbase Account Page",
                         font=LARGE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        pg_title.place(x=420, y=30)

        # Draw data
        # draw account name label
        acct_name_hdr = self.create_label("ACCOUNT NAME:\t\t", 10, 70, True)
        acct_name_lbl = self.create_label(acct.get_acct_name(), 235, 70, False)

        # draw account id label
        acct_id_hdr_lbl = self.create_label("ACCOUNT ID:\t\t", 10, 90, True)
        acct_id_lbl = self.create_label(acct.get_acct_id(), 235, 90, False)

        # draw account balance header 
        acct_bal_hdr = self.create_label("CURRENT ACCOUNT BALANCE:", 10, 110, True)

        # draw account transactions header and table header
        trans_lbl = self.create_label("RECENT TRANSACTIONS", 425, 160, True)
        trans_tbl_lbl = self.create_label(("{0:28s}{1:35s}{2:35s}{3}").format(
                            "TRANSACTION TIME", "TYPE", "AMOUNT", "STATUS"), 215, 195)

        # initiate threads
        self.create_threads()

    def create_label(self, text_param, x_coord, y_coord, bold=False):
        if bold:
            label = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text=text_param, font=HEADER_FONT)
            label.place(x=x_coord, y=y_coord)
        else:
            label = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR, text=text_param)
            label.place(x=x_coord, y=y_coord)

    # continuously updated information needs
    # to be created in a thread here
    def create_threads(self):
        _thread.start_new_thread(self.draw_balance, (acct, 60))
        _thread.start_new_thread(self.draw_transactions, (acct, 60))

    # draw the current account balance to the tkinter window
    def draw_balance(self, account, delay):
        try:
            while 1:
                bal, bal_curr = account.get_acct_balance()
                bal_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                   text=bal + " " + bal_curr) 
                bal_lbl.place(x=235, y=110)
                time.sleep(delay)
        except RuntimeError:
            print("Failed to retrieve balance")
            print("Trying again...")
            self.draw_balance(account, delay)

    # draw the latest account transactions
    def draw_transactions(self, account, delay):
        try:
            while 1:
                trans_lst = account.get_acct_transactions()
                lbl = {}
                count = 0
                spacing = 0

                for t in trans_lst:
                    lbl[count] = self.create_label(
                                    ("{0:30s}{1:10s}{2:13s}{3:6s}" + \
                                    "{4:4s}{5:8s}{6:12s}{7}").format(
                                    trans_lst[count]['created_at'],
                                    trans_lst[count]['type'].upper(),
                                    str(trans_lst[count]['amount']['amount']),
                                    trans_lst[count]['amount']['currency'],
                                    "~",
                                    trans_lst[count]['native_amount']['amount'],
                                    trans_lst[count]['native_amount']['currency'],
                                    trans_lst[count]['status'].upper()),
                                    200, (215 + spacing), False)
                    spacing += 30
                    count += 1

                time.sleep(delay)
        except RuntimeError:
            print("Failed to retrieve transactions")
            print("Trying again...")
            self.draw_transactions(account, delay)





class Data_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)

        # retrieve daily btc prices for
        # past 3 years
        days_delta = data.get_3yr_daily_price()
        lst_prices, lst_dates = data.parse_prices_file(days_delta)

        self.plot_chart(lst_prices, lst_dates)

        # plot controller buttons
        three_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Year",
                command=lambda: self.plot_chart(lst_prices, lst_dates))
        three_yr_btn.place(x=25, y=510)

        one_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="1 Year",
                command=lambda: self.plot_chart(lst_prices[0:365], lst_dates[0:365]))
        one_yr_btn.place(x=100, y=510)

        six_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="6 Month",
                command=lambda: self.plot_chart(lst_prices[0:183], lst_dates[0:183]))
        six_mon_btn.place(x=175, y=510)

        three_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Month",
                command=lambda: self.plot_chart(lst_prices[0:92],lst_dates[0:92]))
        three_mon_btn.place(x=260, y=510)

        one_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="1 Month",
                command=lambda: self.plot_chart(lst_prices[0:30], lst_dates[0:30]))
        one_mon_btn.place(x=345, y=510)

        three_wk_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Week",
                command=lambda: self.plot_chart(lst_prices[0:21],lst_dates[0:21]))
        three_wk_btn.place(x=433, y=510)

        seven_day_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="7 Day",
                command=lambda: self.plot_chart(lst_prices[0:7], lst_dates[0:7]))
        seven_day_btn.place(x=515, y=510)

        #plot misc. conversion data
        # get the currency codes available from cb api 
        # might create a separate function in data class
        rates = data.get_exchange_rates()
        curr_codes = []
        for k,v in rates.items():
            curr_codes.append(k)
        curr_codes.sort()

        xchangert_hdr = self.create_label("Exchange Rate Conversion", 700, 30)

        ''' BTC -> CURRENCY '''
        btc_lbl = self.create_label("BTC  -> ", 690, 60)
        converted_lbl = self.create_label("Converted Amount:", 750, 80)

        # create text entry
        entry = tk.Entry(self, width=10)
        entry.place(x=600, y=60)

        # create currency code combo box
        curr_combo_box = ttk.Combobox(self, state='readonly')
        curr_combo_box['values'] = curr_codes
        curr_combo_box.place(x=750, y=60)

        # create amount label
        converted_amt_var = tk.StringVar()
        converted_amt_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                     textvariable=converted_amt_var)
        converted_amt_lbl.place(x=875, y=80)

        # call the conversion function on btn press
        convert_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="Convert",
                command=lambda: self.convert_currency_btc(entry,
                                                          curr_combo_box,
                                                          converted_amt_var))
        convert_btn.place(x=600, y=80)

        ''' CURRENCY -> BTC '''
        btc_lbl1 = self.create_label("  -> BTC", 875, 150)
        converted_lbl1 = self.create_label("Converted Amount:", 750, 175)

        # create text entry
        entry1 = tk.Entry(self, width=10)
        entry1.place(x=600, y=150)

        # create currency code combo box
        curr_combo_box1 = ttk.Combobox(self, state='readonly')
        curr_combo_box1['values'] = curr_codes
        curr_combo_box1.place(x=695, y=150)

        # create amount label
        converted_amt_var1 = tk.StringVar()
        converted_amt_lbl1 = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                     textvariable=converted_amt_var1)
        converted_amt_lbl1.place(x=875, y=175)

        # call the conversion function on btn press
        convert_btn1 = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="Convert",
                command=lambda: self.convert_currency_oth(entry1,
                                                          curr_combo_box1,
                                                          converted_amt_var1))
        convert_btn1.place(x=600, y=170)

        ''' DRAW MISC BTC DATA '''
        # draw the spot price
        spot_price_lbl = self.create_label("Current Spot Price:", 600, 250)
        buy_price_lbl = self.create_label("Latest Buy Price:", 600, 275) 
        sell_price_lbl = self.create_label("Latest Sell Price:", 600, 300)

        self.start_threads()

    def start_threads(self):
        _thread.start_new_thread(self.draw_spot_price_data, (data, 20))
        _thread.start_new_thread(self.draw_buy_price, (data, 30))
        _thread.start_new_thread(self.draw_sell_price, (data, 30))

    def draw_spot_price_data(self, data, delay):
        while 1:
            spot_price_lst = data.get_spot_price()

            cur_spot_price = spot_price_lst[0] # TEST

            spot_price_lbl = self.create_label((spot_price_lst[0] + " " + \
                                                spot_price_lst[1]), 750, 250)
            time.sleep(delay)

    def draw_buy_price(self, data, delay):
        while 1:
            buy_price = data.get_buy_price()
            buy_price_lbl = self.create_label((buy_price + " USD"), 750, 275)
            time.sleep(delay)

    def draw_sell_price(self, data, delay):
        while 1:
            sell_price = data.get_sell_price()
            sell_price_lbl = self.create_label((sell_price + " USD"), 750, 300)
            time.sleep(delay)

    def create_label(self, text_param, x_coord, y_coord):
        label = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                         text=text_param)
        label.place(x=x_coord, y=y_coord)


    def convert_currency_btc(self, entry_obj, combo_box_obj, convert_amt_var):
        # retrieve user input data
        amount = entry_obj.get()
        code = combo_box_obj.get()

        converted_amt = data.convert_currency_btc(amount, code)

        convert_amt_var.set(("%.2f " + code) % converted_amt)


    def convert_currency_oth(self, entry_obj, combo_box_obj, convert_amt_var):
        # retrieve user input data
        amount = entry_obj.get()
        code = combo_box_obj.get()

        converted_amt = data.convert_currency_oth(amount, code)

        convert_amt_var.set(("%.6f BTC") % converted_amt)


    def plot_chart(self, lst_prices, lst_dates):
        # insert an overview of prices of btc
        # for past 3 years
        f = matplotlib.figure.Figure(figsize=(6,5), dpi=100, facecolor=BG_COLOR)
        a = f.add_subplot(111, ylabel="USD", facecolor=BG_COLOR)

        plot_title = "BTC Prices"
        a.set_title(plot_title, color=FG_COLOR)

        # configure the plot characteristics 
        a.spines['top'].set_color(FG_COLOR)
        a.spines['bottom'].set_color(FG_COLOR)
        a.spines['left'].set_color(FG_COLOR)
        a.spines['right'].set_color(FG_COLOR)
        a.tick_params(axis='x', colors=FG_COLOR, labelsize='small', gridOn=True)
        a.tick_params(axis='y', colors=FG_COLOR, labelsize='small', gridOn=True)
        a.yaxis.label.set_color(FG_COLOR)
        a.xaxis.label.set_color(FG_COLOR)

        a.plot(lst_dates, lst_prices) # plot the data
        
        labels = a.get_xticklabels()
        plt.setp(labels, rotation=30) # rotate labels by 30 deg

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x=0, y=0)




class Analysis_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        title = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                         text="BTC Price Analysis", font=LARGE_FONT)
        title.place(x=400, y=10)

        ''' labels and buttons section '''
        # percent changes labels
        perc_change_lbl = self.create_label("Percent Changes", 700, 50, True)
        one_dy_lbl = self.create_label("24 Hr.:\t", 600, 100)
        one_wk_lbl = self.create_label("1 Wk.:\t", 600, 130)
        three_wk_lbl = self.create_label("3 Wk.:\t", 600, 160)
        one_mn_lbl = self.create_label("1 Mon.:\t", 800, 100)
        three_mn_lbl = self.create_label("3 Mon.:\t", 800, 130)
        six_mn_lbl = self.create_label("6 Mon.:\t", 800, 160)

        # Buy/Sell title and headers
        buy_sell_title = self.create_label("Execute Price Limit Buy/Sell", 650, 200, True)
        buy_sell_status_hdr = self.create_label("Buy/Sell Status: ", 600, 350, True)

        status_msg = tk.StringVar()
        buy_sell_msg_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR, textvariable=status_msg)
        buy_sell_msg_lbl.place(x=600, y=375)

        # account balance lbl



        # plot controller buttons
        three_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Year",
                command=lambda: self.plot_chart_helper(1095,0))
        three_yr_btn.place(x=25, y=510)

        one_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="1 Year",
                command=lambda: self.plot_chart_helper(365, 730))
        one_yr_btn.place(x=100, y=510)

        six_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="6 Month",
                command=lambda: self.plot_chart_helper(184,911))
        six_mon_btn.place(x=175, y=510)

        three_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Month",
                command=lambda: self.plot_chart_helper(92,1003))
        three_mon_btn.place(x=260, y=510)

        one_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="1 Month",
                command=lambda: self.plot_chart_helper(31,1064))
        one_mon_btn.place(x=345, y=510)

        three_wk_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="3 Week",
                command=lambda: self.plot_chart_helper(22,1073))
        three_wk_btn.place(x=433, y=510)

        seven_day_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="7 Day",
                command=lambda: self.plot_chart_helper(7,1087))
        seven_day_btn.place(x=515, y=510)

        # buy/sell execute button
        buy_sell_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="Execute",
                command=lambda: self.initiate_buy_sell_helper(buy_sell_amt_entry, buy_sell_combo,
                                                              currency_combo, status_msg))
        buy_sell_btn.place(x=600, y=300)

        ''' core functionality section '''
        # retrieve regression analysis data for plotting
        lst_total_days, lst_prices, lst_regr_days, lst_regr_prices = analysis.calc_regression(1095,0)
        self.plot_chart(lst_prices, lst_total_days, lst_regr_days, lst_regr_prices)

        # entry box for buy/sell selection
        default_val = tk.StringVar()
        buy_sell_amt_entry = tk.Entry(self, width=15, textvariable=default_val)
        buy_sell_amt_entry.place(x=600, y=260)
        default_val.set("Enter amount")

        # combobox for buy/sell selection
        buy_sell_combo = ttk.Combobox(self, width=10, state="readonly")
        buy_sell_combo["values"] = ["Buy", "Sell"]
        buy_sell_combo.place(x=750, y=260)

        # combobox for currency codes
        xchangert_dict = data.get_exchange_rates()
        currency_lst = []
        for k,v in xchangert_dict.items():
            currency_lst.append(k)
        currency_lst.sort()
        currency_combo = ttk.Combobox(self, width=5, state="readonly")
        currency_combo["values"] = currency_lst
        currency_combo.place(x=850, y=260)


        # start threaded methods
        _thread.start_new_thread(self.draw_perc_change, (30,))

    def initiate_buy_sell_helper(self, buy_sell_amt_entry, buy_sell_combo, currency_combo, status_msg):
        amount = float(buy_sell_amt_entry.get())
        buy_sell = buy_sell_combo.get()
        currency_code = currency_combo.get()

        spot_price = data.get_spot_price()[0]

        if buy_sell == "Buy":
            status_msg.set("You are about to buy " + str(amount) + \
                           " " + currency_code + " at price " + spot_price)
            confirm_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="Confirm",
                                    command=lambda: btn_group_action(amount, currency_code, buy_sell, status_msg))
            confirm_btn.place(x=600, y=410)

        elif buy_sell == "Sell":
            status_msg.set("You are about to sell " + str(amount) + \
                           " " + currency_code + " at price " + spot_price)
            confirm_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR, text="Confirm",
                                    command=lambda: btn_group_action(amount, currency_code, buy_sell, status_msg))
            confirm_btn.place(x=600, y=410)


        def btn_group_action(amount, currency_code, buy_sell, status_msg):
            if buy_sell == "Buy":
                acct.execute_buy(amount, currency_code)
                status_msg.set("Buy order placed.")
                confirm_btn.destroy()
            else:
                acct.execute_sell(amount, currency_code)
                status_msg.set("Sell order placed.")
                confirm_btn.destroy()
                





    def draw_perc_change(self, delay):
        while 1:
            #test_spot_price = data.get_spot_price()
            one_dy_perc_change = analysis.calc_one_dy_change(data)
            one_wk_perc_change = analysis.calc_one_wk_change(data)
            three_wk_perc_change = analysis.calc_three_wk_change(data)
            one_mn_perc_change = analysis.calc_one_mn_change(data)
            three_mn_perc_change = analysis.calc_three_mn_change(data)
            six_mn_perc_change = analysis.calc_six_mn_change(data)

            lst_perc_changes = [one_dy_perc_change, one_wk_perc_change, three_wk_perc_change,
                                one_mn_perc_change, three_mn_perc_change, six_mn_perc_change]

            spacing = 100
            for x in lst_perc_changes[:3]:
                self.create_perc_delta_lbl(x, 675, spacing)
                spacing += 30
            spacing = 100
            for y in lst_perc_changes[3:]:
                self.create_perc_delta_lbl(y, 875, spacing)
                spacing += 30

            time.sleep(delay)


    def create_label(self, text_param, x_coord, y_coord, bold=False):
        if bold:
            label = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text=text_param, font=HEADER_FONT)
            label.place(x=x_coord, y=y_coord)
        else:
            label = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR, text=text_param)
            label.place(x=x_coord, y=y_coord)


    def create_perc_delta_lbl(self, text_param, x_coord, y_coord, increase=False):
        if text_param > 0:
            label = tk.Label(self, bg=BG_COLOR, fg=INC_COLOR,
                             text=("%.2f%%" % text_param))
            label.place(x=x_coord, y=y_coord)
        else:
            label = tk.Label(self, bg=BG_COLOR, fg=DEC_COLOR,
                             text=("%.2f%%" % text_param))
            label.place(x=x_coord, y=y_coord)


    def plot_chart_helper(self, days, prices):
        lst_prices, lst_total_days, lst_regr_days, lst_regr_prices = analysis.calc_regression(days, prices)
        self.plot_chart(lst_total_days, lst_prices, lst_regr_days, lst_regr_prices)


    def plot_chart(self, lst_prices, lst_dates, lst_regr_days, lst_regr_data):
        # insert an overview of prices of btc
        # for past 3 years
        f = matplotlib.figure.Figure(figsize=(6,5), dpi=100, facecolor=BG_COLOR)
        a = f.add_subplot(111, ylabel="USD", facecolor=BG_COLOR)

        plot_title = "BTC Trends"
        a.set_title(plot_title, color=FG_COLOR)

        # configure the plot characteristics 
        a.spines['top'].set_color(FG_COLOR)
        a.spines['bottom'].set_color(FG_COLOR)
        a.spines['left'].set_color(FG_COLOR)
        a.spines['right'].set_color(FG_COLOR)
        a.tick_params(axis='x', colors=FG_COLOR, labelsize='small', gridOn=True)
        a.tick_params(axis='y', colors=FG_COLOR, labelsize='small', gridOn=True)
        a.yaxis.label.set_color(FG_COLOR)
        a.xaxis.label.set_color(FG_COLOR)

        a.plot(lst_dates, lst_prices) # plot the data

        # if-else condition set for trendline color
        if lst_regr_data[0] > lst_regr_data[1]:
            a.plot(lst_regr_days, lst_regr_data, ls="--", lw=0.75, color=DEC_COLOR)
        else:
            a.plot(lst_regr_days, lst_regr_data, ls="--", lw=0.75, color=INC_COLOR)
        
        labels = a.get_xticklabels()
        plt.setp(labels, rotation=30) # rotate labels by 30 deg

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x=0, y=0)



if __name__ == '__main__':
    # instantiate core class objects
    data = Data()
    acct = Account()
    analysis = Analysis()
    app = Gui()

    app.geometry(str(WIN_LENGTH) + "x" + str(WIN_WIDTH))
    app.mainloop()


