'''
Gui class created with Tkinter
'''
# thread related imports
import _thread
import time

# gui module imports
import tkinter as tk
from tkinter import ttk

# backend class imports
from account import Account
#from analysis import Analysis
from data import Data

# gui globals
LARGE_FONT = ("Free Sans", 12)
HEADER_FONT = ("Free Sans", 10, 'bold')
WIN_LENGTH = 1000 
WIN_WIDTH = 600

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

        for fm in (Main_Page, Account_Page, Data_Page):
            frame = fm(container, self)
            self.frames[fm] = frame
            frame.grid(row=0, column=0, sticky='nsew')  # sticky (stretch win items north
                                                        # south east west)
        self.show_frame(Main_Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Coinbase Trading Application", font=LARGE_FONT)
        label.place(x=(WIN_LENGTH/2 - 100), y=30)
        #label.pack(pady=10, padx=10)

        acct_btn = ttk.Button(self, text="Coinbase Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        acct_btn.place(x=0, y=0)

        data_btn = ttk.Button(self, text="BTC Data Information",
                            command=lambda: controller.show_frame(Data_Page))
        data_btn.place(x=300, y=0)

        # instantiate primary objects
        acct_1 = Account()
        data_1 = Data()

        # Draw data
        # draw account name label
        acct_name_lbl = tk.Label(self, text="ACCOUNT NAME:\t\t" + acct_1.get_acct_name())
        acct_name_lbl.place(x=(WIN_LENGTH / 100), y=50)

        # draw account id label
        acct_id_lbl = tk.Label(self, text="ACCOUNT ID:\t\t" + acct_1.get_acct_id())
        acct_id_lbl.place(x=(WIN_LENGTH / 100), y=70)

        # 1st thread (draw account balance)
        _thread.start_new_thread(self.draw_balance, (acct_1, 60))

        # 2nd thread (draw account transactions)
        trans_lbl = tk.Label(self, text="RECENT TRANSACTIONS", font=HEADER_FONT)
        trans_lbl.place(x=(WIN_LENGTH / 2 - 50), y=140)
        _thread.start_new_thread(self.draw_transactions, (acct_1, 60))

        # 3rd thread (draw current spot price)
        price_lbl = tk.Label(self, text="CURRENT BTC PRICE: ")
        price_lbl.place(x=(WIN_LENGTH - 250), y=50)
        _thread.start_new_thread(self.draw_spot_price, (data_1, 30))

    # draw the current account balance to the tkinter window
    def draw_balance(self, account, delay):
        while 1:
            bal, bal_curr = account.get_acct_balance()
            bal_lbl = tk.Label(self, text="Current Account Balance:\t" + \
                               bal + " " + bal_curr)
            bal_lbl.place(x=(WIN_LENGTH / 100), y=90)
            time.sleep(delay)

    def draw_spot_price(self, data, delay):
        while 1:
            spot_price_lst = data.get_spot_price()
            spot_price_lbl = tk.Label(self, text=spot_price_lst[0] + \
                                      " " + spot_price_lst[1])
            spot_price_lbl.place(x=(WIN_LENGTH - 100), y = 50)
            time.sleep(delay)

    # draw the latest account transactions
    def draw_transactions(self, account, delay):
        while 1:
            trans_lst = account.get_acct_transactions()
            lbl = {}
            spacing = 0

            for i in range(5):
                key_str = 'trans' + str(i) + '_lbl'
                lbl[key_str] = tk.Label(self,
                                        text="{0}\t{1}\t{2} {3} ~ {4} {5}\t\t{6}".format(
                                        trans_lst[i]['created_at'],
                                        trans_lst[i]['type'].upper(),
                                        str(trans_lst[i]['amount']['amount']),
                                        trans_lst[i]['amount']['currency'],
                                        trans_lst[i]['native_amount']['amount'],
                                        trans_lst[i]['native_amount']['currency'],
                                        trans_lst[i]['status']))
                lbl[key_str].place(x=(WIN_WIDTH // 4), y=(160 + spacing))
                spacing += 20

            time.sleep(delay)






class Account_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Coinbase Account Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="BTC Data Information",
                            command=lambda: controller.show_frame(Data_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Back to Main Page",
                            command=lambda: controller.show_frame(Main_Page))
        button2.pack()


class Data_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BTC Data Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Coinbase Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Back to Main Page",
                            command=lambda: controller.show_frame(Main_Page))
        button2.pack()


# Run the script
app = Gui()
app.geometry(str(WIN_LENGTH) + "x" + str(WIN_WIDTH))
app.mainloop()


