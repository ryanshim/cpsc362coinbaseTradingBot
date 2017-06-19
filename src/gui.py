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

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "CB Trading Bot")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)    # 0 is min size
                                                    # weight is priority (just use 1)
        container.grid_columnconfigure(0, weight=1)

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

        # create navigation buttons
        acct_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                            text="CB Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        acct_btn.place(x=65, y=500)

        data_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                              text="BTC Data Information",
                              command=lambda: controller.show_frame(Data_Page))
        data_btn.place(x=325, y=500)

        analysis_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                                  text="BTC Buy/Sell Analysis",
                                  command=lambda: controller.show_frame(Analysis_Page))
        analysis_btn.place(x=585, y=500)

        exit_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                              text="EXIT", command=quit)
        exit_btn.place(x=845, y=500)

        # instantiate primary object
        data_1 = Data()

        # display last spot price
        price_lbl = tk.Label(self, text="Last BTC price: ", bg=BG_COLOR, fg=FG_COLOR)
        price_lbl.place(x=(WIN_LENGTH // 2 - 150), y=65)
        _thread.start_new_thread(self.draw_spot_price_main, (data_1, 30))

        # retrieve daily btc prices for
        # past 3 years
        days_delta = data_1.get_3yr_daily_price()
        lst_prices, lst_dates = data_1.parse_prices_file(days_delta)

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
        canvas.get_tk_widget().place(x=(WIN_LENGTH // 10), y=80)

        # matplotlib toolbar
        '''
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x=(WIN_LENGTH // 10), y=80)
        '''

    def draw_spot_price_main(self, data, delay):
        while 1:
            spot_price_lst = data.get_spot_price()
            spot_price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                      text=spot_price_lst[0] + \
                                      " " + spot_price_lst[1])
            spot_price_lbl.place(x=(WIN_LENGTH // 2 + 50), y = 65)
            time.sleep(delay)





'''
Account information page
'''
class Account_Page(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Coinbase Account Page",
                         font=LARGE_FONT, bg=BG_COLOR, fg=FG_COLOR)
        label.place(x=(WIN_LENGTH/2 - 100), y=30)

        main_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="Back to Main Page",
                             command=lambda: controller.show_frame(Main_Page))
        main_btn.place(x=325, y=500)

        data_btn = tk.Button(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="BTC Data Information",
                             command=lambda: controller.show_frame(Data_Page))
        data_btn.place(x=65, y=500)

        # instantiate primary objects
        acct_1 = Account()
        data_1 = Data()

        # Draw data
        # draw account name label
        acct_name_hdr = tk.Label(self, text="ACCOUNT NAME:\t\t",
                                 font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR)
        acct_name_hdr.place(x=(WIN_LENGTH / 100), y=50)
        acct_name_lbl = tk.Label(self, text=acct_1.get_acct_name(),
                                 bg=BG_COLOR, fg=FG_COLOR)
        acct_name_lbl.place(x=(WIN_LENGTH / 100 + 225), y=50)

        # draw account id label
        acct_id_hdr_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                   text="ACCOUNT ID:\t\t",
                                   font=HEADER_FONT)
        acct_id_hdr_lbl.place(x=(WIN_LENGTH / 100), y=70)
        acct_id_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                               text=acct_1.get_acct_id())
        acct_id_lbl.place(x=(WIN_LENGTH / 100 + 225), y=70)

        # draw account balance header 
        acct_bal_hdr = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                text="CURRENT ACCOUNT BALANCE:",
                                font=HEADER_FONT)
        acct_bal_hdr.place(x=(WIN_LENGTH / 100), y=90)

        # draw current spot price header
        price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="CURRENT BTC PRICE: ",
                             font=HEADER_FONT)
        price_lbl.place(x=(WIN_LENGTH - 250), y=50)

        # draw account transactions header
        trans_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                             text="RECENT TRANSACTIONS", font=HEADER_FONT)
        trans_lbl.place(x=(WIN_LENGTH / 2 - 75), y=145)

        # 1st thread (draw account balance)
        _thread.start_new_thread(self.draw_balance, (acct_1, 60))

        # 2nd thread (draw account transactions)
        _thread.start_new_thread(self.draw_transactions, (acct_1, 60))

        # 3rd thread (draw current spot price)
        _thread.start_new_thread(self.draw_spot_price, (data_1, 30))

    # initiate threads function
    #def create_threads(self, )

    # draw the current account balance to the tkinter window
    def draw_balance(self, account, delay):
        while 1:
            bal, bal_curr = account.get_acct_balance()
            bal_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                               text=bal + " " + bal_curr) 
            bal_lbl.place(x=(WIN_LENGTH / 100 + 225), y=90)
            time.sleep(delay)

    def draw_spot_price(self, data, delay):
        while 1:
            spot_price_lst = data.get_spot_price()
            spot_price_lbl = tk.Label(self, bg=BG_COLOR, fg=FG_COLOR,
                                      text=spot_price_lst[0] + \
                                      " " + spot_price_lst[1])
            spot_price_lbl.place(x=(WIN_LENGTH - 100), y = 50)
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
                                      text="{0:30s}{1:10s}{2:13s}{3:6s}{4:4s}{5:8s}{6:12s}{7}".format(
                                      trans_lst[count]['created_at'],
                                      trans_lst[count]['type'].upper(),
                                      str(trans_lst[count]['amount']['amount']),
                                      trans_lst[count]['amount']['currency'],
                                      "~",
                                      trans_lst[count]['native_amount']['amount'],
                                      trans_lst[count]['native_amount']['currency'],
                                      trans_lst[count]['status'].upper()))
                lbl[count].place(x=(WIN_WIDTH // 2.5), y=(170 + spacing))
                spacing += 30
                count += 1

            time.sleep(delay)


class Data_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="BTC Data Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Coinbase Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Back to Main Page",
                            command=lambda: controller.show_frame(Main_Page))
        button2.pack()


class Analysis_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="BTC Analysis Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Coinbase Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Back to Main Page",
                            command=lambda: controller.show_frame(Data_Page))
        button2.pack()

        button3 = ttk.Button(self, text="Back to Main Page",
                            command=lambda: controller.show_frame(Main_Page))
        button3.pack()




# Run the script
app = Gui()
app.geometry(str(WIN_LENGTH) + "x" + str(WIN_WIDTH))
app.mainloop()


