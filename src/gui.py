'''
Gui class created with Tkinter
'''
# thread related imports
import _thread
import time

# gui module imports
import tkinter as tk
from tkinter import ttk

# matplot lib imports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg 

# backend class imports
from account import Account
#from analysis import Analysis
from data import Data

# gui globals
LARGE_FONT = ("Free Sans", 12)
HEADER_FONT = ("Free Sans", 10, 'bold')
WIN_LENGTH = 1000 
WIN_WIDTH = 600
BG_COLOR = "#FFFFFF"
FG_COLOR = "#303642"


spot_price_var = []

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
        file_menu.add_command(label="CB Account", command=lambda: self.show_frame(Account_Page))
        file_menu.add_separator()
        file_menu.add_command(label="BTC Data", command=lambda: self.show_frame(Data_Page))
        file_menu.add_separator()
        file_menu.add_command(label="BTC Analysis", command=lambda: self.show_frame(Analysis_Page))
        file_menu.add_separator()
        file_menu.add_command(label="Main Page", command=lambda: self.show_frame(Main_Page))
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
        label.place(x=(WIN_LENGTH/2 - 100), y=30)

        # display last spot price
        price_lbl = tk.Label(self, text="Last BTC price: ", bg=BG_COLOR, fg=FG_COLOR)
        price_lbl.place(x=410, y=65)

        # retrieve daily btc prices for
        # past 3 years
        days_delta = data.get_3yr_daily_price()
        lst_prices, lst_dates = data.parse_prices_file(days_delta)

        self.start_threads_main()

        # insert an overview of prices of btc
        # for past 3 years
        f = matplotlib.figure.Figure(figsize=(8,4), dpi=100, facecolor=BG_COLOR)
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
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x=100, y=80)

        '''
        # matplotlib toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x=(WIN_LENGTH // 10), y=80)
        '''

    def start_threads_main(self):
        _thread.start_new_thread(self.retrieve_spot_price, (data, 30))

    def retrieve_spot_price(self, cls_data, delay):
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
        label = tk.Label(self, text="Coinbase Account Page",
                         font=LARGE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        label.place(x=420, y=30)


        # Draw data
        # draw account name label
        acct_name_hdr = tk.Label(self, text="ACCOUNT NAME:\t\t",
                                 font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR)
        acct_name_hdr.place(x=10, y=70)
        acct_name_lbl = tk.Label(self, text=acct.get_acct_name(),
                                 bg=BG_COLOR, fg=FG_COLOR)
        acct_name_lbl.place(x=235, y=70)

        # draw account id label
        acct_id_hdr_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                   text="ACCOUNT ID:\t\t",
                                   font=HEADER_FONT)
        acct_id_hdr_lbl.place(x=10, y=90)
        acct_id_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                               text=acct.get_acct_id())
        acct_id_lbl.place(x=235, y=90)

        # draw account balance header 
        acct_bal_hdr = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                text="CURRENT ACCOUNT BALANCE:",
                                font=HEADER_FONT)
        acct_bal_hdr.place(x=10, y=110)

        # draw current spot price header
        price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="CURRENT BTC PRICE: ",
                             font=HEADER_FONT)
        price_lbl.place(x=750, y=70)

        # draw account transactions header and table header
        trans_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="RECENT TRANSACTIONS", font=HEADER_FONT)
        trans_lbl.place(x=425, y=160)
        trans_tbl_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text=("{0:28s}{1:35s}{2:35s}{3}").format(
                                 "TRANSACTION TIME",
                                 "TYPE",
                                 "AMOUNT",
                                 "STATUS"))
        trans_tbl_lbl.place(x=215, y=195)


        self.create_threads()

    # initiate threads function
    def create_threads(self):
        _thread.start_new_thread(self.draw_balance, (acct, 60))
        _thread.start_new_thread(self.draw_transactions, (acct, 60))
        _thread.start_new_thread(self.draw_spot_price, (data, 30))

    # draw the current account balance to the tkinter window
    def draw_balance(self, account, delay):
        while 1:
            bal, bal_curr = account.get_acct_balance()
            bal_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                               text=bal + " " + bal_curr) 
            bal_lbl.place(x=235, y=110)
            time.sleep(delay)

    def draw_spot_price(self, data, delay):
        while 1:
            spot_price_lst = data.get_spot_price()
            spot_price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                      text=spot_price_lst[0] + \
                                      " " + spot_price_lst[1])
            spot_price_lbl.place(x=900, y = 70)
            time.sleep(delay)

    # draw the latest account transactions
    def draw_transactions(self, account, delay):
        while 1:
            trans_lst = account.get_acct_transactions()
            lbl = {}
            count = 0
            spacing = 0

            for t in trans_lst:
                lbl[count] = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                      text=("{0:30s}{1:10s}{2:13s}{3:6s}" + \
                                            "{4:4s}{5:8s}{6:12s}{7}").format(
                                      trans_lst[count]['created_at'],
                                      trans_lst[count]['type'].upper(),
                                      str(trans_lst[count]['amount']['amount']),
                                      trans_lst[count]['amount']['currency'],
                                      "~",
                                      trans_lst[count]['native_amount']['amount'],
                                      trans_lst[count]['native_amount']['currency'],
                                      trans_lst[count]['status'].upper()))
                lbl[count].place(x=200, y=(215 + spacing))
                spacing += 30
                count += 1

            time.sleep(delay)


class Data_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)

        # retrieve daily btc prices for
        # past 3 years
        days_delta = data.get_3yr_daily_price()

        lst_prices, lst_dates = data.parse_prices_file(days_delta)

        self.plot_chart(lst_prices, lst_dates)

        # plot controller buttons
        three_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="3 Year",
                                 command=lambda: self.plot_chart(lst_prices, lst_dates))
        three_yr_btn.place(x=25, y=400)

        one_yr_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="1 Year",
                                 command=lambda: self.plot_chart(lst_prices[0:365],
                                                                 lst_dates[0:365]))
        one_yr_btn.place(x=100, y=400)

        six_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="6 Month",
                                 command=lambda: self.plot_chart(lst_prices[0:183],
                                                                 lst_dates[0:183]))
        six_mon_btn.place(x=175, y=400)

        three_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="3 Month",
                                 command=lambda: self.plot_chart(lst_prices[0:92],
                                                                 lst_dates[0:92]))
        three_mon_btn.place(x=260, y=400)

        one_mon_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="1 Month",
                                 command=lambda: self.plot_chart(lst_prices[0:30],
                                                                 lst_dates[0:30]))
        one_mon_btn.place(x=345, y=400)

        three_wk_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="3 Week",
                                 command=lambda: self.plot_chart(lst_prices[0:21],
                                                                 lst_dates[0:21]))
        three_wk_btn.place(x=433, y=400)

        seven_day_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                 text="7 Day",
                                 command=lambda: self.plot_chart(lst_prices[0:7],
                                                                 lst_dates[0:7]))
        seven_day_btn.place(x=515, y=400)


    def plot_chart(self, lst_prices, lst_dates):
        # insert an overview of prices of btc
        # for past 3 years
        f = matplotlib.figure.Figure(figsize=(6,3), dpi=100, facecolor=BG_COLOR)
        a = f.add_subplot(111, ylabel="USD", facecolor=BG_COLOR)

        plot_title = "BTC Prices"
        a.set_title(plot_title, color=FG_COLOR)

        a.spines['top'].set_color(FG_COLOR)
        a.spines['bottom'].set_color(FG_COLOR)
        a.spines['left'].set_color(FG_COLOR)
        a.spines['right'].set_color(FG_COLOR)
        a.tick_params(axis='x', colors=FG_COLOR, which='major')
        a.tick_params(axis='y', colors=FG_COLOR)
        a.yaxis.label.set_color(FG_COLOR)
        a.xaxis.label.set_color(FG_COLOR)

        a.plot(lst_dates, lst_prices)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(x=20, y=20)




class Analysis_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="BTC Analysis Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)




if __name__ == '__main__':
    # instantiate core class objects
    data = Data()
    acct = Account()
    app = Gui()

    app.geometry(str(WIN_LENGTH) + "x" + str(WIN_WIDTH))
    app.mainloop()




