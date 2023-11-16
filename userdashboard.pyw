import customtkinter
from pymongo import *
import hashlib
from tkinter import messagebox
import arrow

Client = MongoClient("connection string")
Database = Client['db name']
Clients_Collection = Database['Collection name']
Transactions_Collection = Database['Collection name']
def UserDashboard():

    def upadteTime():
        today_date_label.configure(text=f"today is : {arrow.now().format('DD/MM/YYYY HH:mm')}")
        today_date_label.after(25000, upadteTime)
    def fetchUpdate():
        global fetchuser
        fetchuser = Clients_Collection.find_one({'Username': fetch_users['Username']})
        saving_bal = fetchuser['Savings']
        spending_bal = fetchuser['Balance']
        spending_balance.configure(text=f'{spending_bal} $')
        savings_balance.configure(text=f'{saving_bal} $')
        spending_balance.after(30000, fetchUpdate)
        savings_balance.after(30000, fetchUpdate)
        spending_lenght = len(str(spending_bal))
        savings_lenght = len(str(saving_bal))
        if spending_lenght > 6 or savings_lenght > 6:
            spending_balance.place(x=105, y=31)
            savings_balance.place(x=400, y=31)
        else:
            spending_balance.place(x=105, y=31)
            savings_balance.place(x=405, y=31)
    def sendTransfer():
        reciver = userName.get()
        transferamount = amount.get()
        sender = fetchuser
        sender_balance = sender['Balance']
        check_reciver = Clients_Collection.find_one({'Username': reciver})
        if check_reciver:
            reciver_balance = check_reciver['Balance']
            if float(transferamount) > float(sender_balance):
                messagebox.showerror(title="Error", message="Insufficient Balance!")
            else:
                time = arrow.now().format('DD/MM/YY HH:mm:ss')
                Clients_Collection.update_one({"Username": sender['Username']},{"$set": {"Balance": float(sender_balance) - float(transferamount)}})
                Clients_Collection.update_one({'Username': reciver}, {"$set": {'Balance': float(reciver_balance) + float(transferamount)}})
                Transactions_Collection.insert_one({'From': sender['Username'], 'To': reciver, "Amount": transferamount, 'Timestamp': time, 'Type': "Transfer"})
                messagebox.showinfo(title="Success", message=f"Successfully sent : {transferamount} $ to  {reciver}")
        else:
            messagebox.showwarning(title="Warning!", message="Reciver Not found")
    def Transfer():
        global userName
        global amount
        window = customtkinter.CTkToplevel()
        window.focus_get()
        window.geometry('400x350')
        window.resizable(False, False)
        window.title("Transfer")
        userName = customtkinter.CTkEntry(master=window, width=250, height=40, placeholder_text="Username")
        userName.place(x=70,y=30)
        amount = customtkinter.CTkEntry(master=window, width=250, height=40, placeholder_text="Amount")
        amount.place(x=70,y=85)
        transferBTN = customtkinter.CTkButton(master=window, width=250, height=40, text="Send Transfer", command=sendTransfer)
        transferBTN.place(x=70, y=145)
        window.focus_set()
        window.grab_set()
    def Withdraw():
        pass
    def sendSavings():
        sender = fetchuser
        time = arrow.now().format('DD/MM/YY HH:mm:ss')
        sender_saving_bal = sender['Savings']
        sender_spending_bal = sender['Balance']
        get_amount = internaltransfer.get()
        if float(get_amount) > sender_spending_bal:
            messagebox.showerror(title='Error', message="Insufficient Balance!")
        else:
            hash_user = hashlib.sha384(sender['Username'].encode('utf-8')).hexdigest()
            Clients_Collection.update_one({'Username': sender['Username']}, {"$set": {'Savings': float(sender_saving_bal) + float(get_amount)}})
            Clients_Collection.update_one({'Username': sender['Username']}, {'$set': {'Balance': float(sender_spending_bal) - float(get_amount)}})
            Transactions_Collection.insert_one({'Username': hash_user, 'Amount': float(get_amount), 'Type': "Internal Transfer", 'Timestamp': time})
            messagebox.showinfo(title="Success", message=f"Successfully sended {get_amount} $ to savings")
    def sendSpending():
        sender = fetchuser
        time = arrow.now().format('DD/MM/YY HH:mm:ss')
        sender_saving_bal = sender['Savings']
        sender_spending_bal = sender['Balance']
        get_amount = internaltransfer.get()
        if float(get_amount) > sender_spending_bal:
            messagebox.showerror(title='Error', message="Insufficient Balance!")
        else:
            hash_user = hashlib.sha384(sender['Username'].encode('utf-8')).hexdigest()
            Clients_Collection.update_one({'Username': sender['Username']}, {"$set": {'Balance': float(sender_spending_bal) + float(get_amount)}})
            Clients_Collection.update_one({'Username': sender['Username']}, {'$set': {'Savings': float(sender_saving_bal) - float(get_amount)}})
            Transactions_Collection.insert_one({'Username': hash_user, 'Amount': float(get_amount), 'Type': "Internal Transfer", 'Timestamp': time})
            messagebox.showinfo(title="Success", message=f"Successfully sended {get_amount} $ to spending")
    def Savings():
        global userName
        global internaltransfer
        window = customtkinter.CTkToplevel()
        window.focus_get()
        window.geometry('400x350')
        window.resizable(False, False)
        window.title("Savings")
        label = customtkinter.CTkLabel(master=window, text="Send to Savings")
        label.place(x=155, y=60)
        internaltransfer = customtkinter.CTkEntry(master=window, width=250, height=40, placeholder_text="Amount")
        internaltransfer.place(x=70,y=85)
        transferBTN = customtkinter.CTkButton(master=window, width=250, height=40, text="Send to Savings", command=sendSavings)
        transferBTN.place(x=70, y=145)
        window.focus_set()
        window.grab_set()
    
    def Spending():
        global userName
        global internaltransfer
        window = customtkinter.CTkToplevel()
        window.focus_get()
        window.geometry('400x350')
        window.resizable(False, False)
        window.title("Spending")
        label = customtkinter.CTkLabel(master=window, text="Send to Spending")
        label.place(x=155, y=60)
        internaltransfer = customtkinter.CTkEntry(master=window, width=250, height=40, placeholder_text="Amount")
        internaltransfer.place(x=70,y=85)
        transferBTN = customtkinter.CTkButton(master=window, width=250, height=40, text="Send to Spending", command=sendSpending)
        transferBTN.place(x=70, y=145)
        window.focus_set()
        window.grab_set()
    def logout():
        app.destroy()
    global app
    root.destroy()
    app = customtkinter.CTk(fg_color="#191919")
    app.geometry('690x500')
    app.title('User Dashboard')
    app.resizable(False, False)

    top_panel = customtkinter.CTkFrame(master=app, width=680, height=95, corner_radius=10, fg_color='#242424')
    top_panel.place(x=5, y=5)

    user_label = customtkinter.CTkLabel(master=top_panel, text=f'Welcome back :  {fetch_users["Username"]}!', font=('Arial', 25), fg_color='#242424', bg_color='#242424')
    user_label.place(x=10, y=10)
    today_date = arrow.now().format('DD/MM/YYYY HH:mm')
    today_date_label = customtkinter.CTkLabel(master=top_panel, text=f"today is : {today_date}", font=('Arial', 15), fg_color='#242424', bg_color='#242424')
    today_date_label.place(x=10, y=35)

    vertical_panel = customtkinter.CTkFrame(master=app,width=125, height=385, corner_radius=10, fg_color='#242424')
    vertical_panel.place(x=5, y=105)

    second_top_panel = customtkinter.CTkFrame(master=app, width=550, height=75, corner_radius=10, fg_color='#242424')
    second_top_panel.place(x=135, y=105)

    second_top_panel_divider = customtkinter.CTkFrame(master=second_top_panel, width=4, height=65, corner_radius=0, fg_color='#FFFFFF')
    second_top_panel_divider.place(x=275, y=5)

    spending_label = customtkinter.CTkLabel(master=second_top_panel, text='Spending', font=('Arial', 16), fg_color='#242424', bg_color='#242424')
    spending_label.place(x=100, y=5)

    savings_label = customtkinter.CTkLabel(master=second_top_panel, text='Savings', font=('Arial', 16), fg_color='#242424', bg_color='#242424')
    savings_label.place(x=400, y=5)

    spending_balance = customtkinter.CTkLabel(master=second_top_panel, font=('Arial', 16), fg_color='#242424', bg_color='#242424')
    spending_balance.place(x=1150, y=31)

    savings_balance = customtkinter.CTkLabel(master=second_top_panel, font=('Arial', 16), fg_color='#242424', bg_color='#242424')
    savings_balance.place(x=410, y=31)

    transferBTN = customtkinter.CTkButton(master=vertical_panel, width=113, height=40, text="Transfer", bg_color='#242424',fg_color="#279EFF", corner_radius=10, border_width=0, command=Transfer)
    transferBTN.place(x=7,y=100)

    withdrawBTN = customtkinter.CTkButton(master=vertical_panel, width=113, height=40, text="Withdraw", bg_color='#242424',fg_color="#279EFF", corner_radius=10, border_width=0,)
    withdrawBTN.place(x=7,y=150)

    savingsBTN = customtkinter.CTkButton(master=vertical_panel, width=113, height=40, text="Send to savings", bg_color='#242424',fg_color="#279EFF", corner_radius=10, border_width=0,command=Savings)
    savingsBTN.place(x=7,y=200)

    normalBTN = customtkinter.CTkButton(master=vertical_panel, width=113, height=40, text="Send to Spending", bg_color='#242424',fg_color="#279EFF", corner_radius=10, border_width=0,command=Spending, font=('Arial', 11))
    normalBTN.place(x=7,y=250)
    
    LogouytBTN = customtkinter.CTkButton(master=vertical_panel, width=113, height=40, text="Logout", bg_color='#242424',fg_color="#279EFF", corner_radius=10, border_width=0, command=logout)
    LogouytBTN.place(x=7,y=335)

    app.after(0, fetchUpdate)
    app.after(0, upadteTime)
    app.mainloop()

def userForm():

    global root
    global login_btn
    global not_usr_btn
    global not_usr_label
    global user_name
    global user_password

    root = customtkinter.CTk(fg_color="#191919")
    root.title('User Form')
    root.geometry('400x500')
    root.resizable(False, False)

    panel = customtkinter.CTkFrame(master=root, width=350, height=500, corner_radius=15, fg_color='#242424')
    panel.pack(pady=50)

    bank_name = customtkinter.CTkLabel(master=root, text='Flow Bank', font=('Arial', 25), fg_color='#191919', bg_color='#191919',)
    bank_name.place(x=150, y=20)

    user_name = customtkinter.CTkEntry(master=panel, width=300, height=45, corner_radius=13, border_width=0, placeholder_text="Username")
    user_name.place(x=25, y=50)

    user_password = customtkinter.CTkEntry(master=panel, width=300, height=45, corner_radius=13, border_width=0, placeholder_text="Password", show="*")
    user_password.place(x=25, y=110)
    
    not_usr_label = customtkinter.CTkLabel(master=panel, text='Not a user?', font=('Arial', 12), fg_color='#242424', bg_color='#242424')
    not_usr_label.place(x=30, y=165)

    not_usr_btn = customtkinter.CTkButton(master=panel, width=65, height=15, text="Sign Up", fg_color='#242424', bg_color='#242424', corner_radius=0, border_width=0,hover_color='#242424', command=switch_to_register)
    not_usr_btn.place(x=105, y=168)

    separator = customtkinter.CTkFrame(master=panel, width=300, height=4, corner_radius=0, fg_color='#FFFFFF')
    separator.place(x=25, y=205)

    login_btn = customtkinter.CTkButton(master=panel, width=300, height=45, text="Login", fg_color='#279EFF', corner_radius=13, border_width=0, command=Login)
    login_btn.place(x=25,y=230)

    root.mainloop()
def switch_to_register():
    not_usr_label.configure(text="Already an user?")
    not_usr_btn.configure(text="Login")
    login_btn.configure(text="Register")
    not_usr_btn.configure(command=switch_to_login)
    not_usr_btn.place(x=145, y=168)
    login_btn.configure(command=Register)
def switch_to_login():
    not_usr_label.configure(text="Not an user?")
    not_usr_btn.configure(text="Register")
    login_btn.configure(text="Login")
    not_usr_btn.configure(command=switch_to_register)
    login_btn.configure(command=Login)
def Login():
    global fetch_users
    get_username = user_name.get()
    get_password = user_password.get()
    if get_username == "" or get_password == "":
        messagebox.showerror(title="Error", message="Fill all fields!")
    else:
        fetch_users = Clients_Collection.find_one({'Username': get_username})
        if fetch_users:
            hash_password = hashlib.sha512(get_password.encode('utf-8')).hexdigest()
            if hash_password == fetch_users['Password']:
                messagebox.showinfo(title='Success', message='Successfully Logged in!')
                UserDashboard()
            else:
                messagebox.showerror(title='Error', message='Wrong Password!')
        else:
            messagebox.showerror(title='Error', message='User not found!')
def Register():
    get_username = user_name.get()
    get_password = user_password.get()
    hash_password = hashlib.sha512(get_password.encode('utf-8')).hexdigest()
    fetch_users = Clients_Collection.find_one({'Username': get_username})
    if get_password == "" or get_password == "":
        messagebox.showerror(title="Error", message="Fill all fields!")
    else:
        if fetch_users:
            messagebox.showerror(title="error", message="User already registred!")
        else:
            Clients_Collection.insert_one({'Username': get_username, 'Password': hash_password, 'Balance': 0.00,'Savings': 0.00, 'Privilege': 'user'})
            messagebox.showinfo(title='Success', message='Successfully Registered account!')
userForm()