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

LARGE_FONT = ("Free Sans", 12)

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
            frame.grid(row=0, column=0, sticky='nsew') # sticky (stretch win items north

        self.show_frame(Main_Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Coinbase Trading Application", font=LARGE_FONT)
        label.place(x=400, y=30)
        #label.pack(pady=10, padx=10)

        acct_btn = ttk.Button(self, text="Coinbase Account Information",
                            command=lambda: controller.show_frame(Account_Page))
        acct_btn.place(x=0, y=0)

        data_btn = ttk.Button(self, text="BTC Data Information",
                            command=lambda: controller.show_frame(Data_Page))
        data_btn.place(x=300, y=0)

        # create account object
        acct_1 = Account()

        # Draw data
        # draw account name label
        acct_name_lbl = tk.Label(self, text="ACCOUNT NAME: " + acct_1.get_acct_name())
        acct_name_lbl.place(x=10, y=50)

        # draw account id label
        acct_id_lbl = tk.Label(self, text="ACCOUNT ID: " + acct_1.get_acct_id())
        acct_id_lbl.place(x=10, y=70)

        # 1st thread (draw account balance)
        _thread.start_new_thread(self.draw_balance, (acct_1, 30))
        # 2nd thread (draw account transactions)
        trans_title_lbl = tk.Label(self, text="RECENT TRANSACTIONS")
        trans_title_lbl.place(x=10, y=140)
        _thread.start_new_thread(self.draw_transactions, (acct_1, 30))


    # draw the current account balance to the tkinter window
    def draw_balance(self, account, delay):
        while 1:
            bal, bal_curr = account.get_acct_balance()
            bal_lbl = tk.Label(self, text="Current Account Balance: " + bal + bal_curr)
            bal_lbl.place(x=10, y=90)
            time.sleep(delay)

    # draw the latest account transactions
    def draw_transactions(self, account, delay):
        while 1:
            trans_lst = account.get_acct_transactions()

            trans1_lbl = tk.Label(self, text=str(trans_lst[0]['amount']['amount']) + \
                                  " " + trans_lst[0]['amount']['currency'] + \
                                  "\t" + trans_lst[0]['type'] + \
                                  "\t" + trans_lst[0]['status'])
            trans1_lbl.place(x=10, y=160)

            trans2_lbl = tk.Label(self, text=str(trans_lst[1]['amount']['amount']) + \
                                  " " + trans_lst[1]['amount']['currency'] + \
                                  "\t" + trans_lst[1]['type'] + \
                                  "\t" + trans_lst[1]['status'])
            trans2_lbl.place(x=10, y=180)

            trans3_lbl = tk.Label(self, text=str(trans_lst[2]['amount']['amount']) + \
                                  " " + trans_lst[2]['amount']['currency'] + \
                                  "\t" + trans_lst[2]['type'] + \
                                  "\t" + trans_lst[2]['status'])
            trans3_lbl.place(x=10, y=200)

            trans4_lbl = tk.Label(self, text=str(trans_lst[3]['amount']['amount']) + \
                                  " " + trans_lst[3]['amount']['currency'] + \
                                  "\t" + trans_lst[3]['type'] + \
                                  "\t" + trans_lst[3]['status'])
            trans4_lbl.place(x=10, y=220)

            trans5_lbl = tk.Label(self, text=str(trans_lst[4]['amount']['amount']) + \
                                  " " + trans_lst[4]['amount']['currency'] + \
                                  "\t" + trans_lst[4]['type'] + \
                                  "\t" + trans_lst[4]['status'])
            trans5_lbl.place(x=10, y=240)








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
app.geometry("1000x600")

app.mainloop()


