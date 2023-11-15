import customtkinter
from pymongo import *
import hashlib
from tkinter import messagebox

Client = MongoClient("connection string")
Database = Client['Your database name']
Clients_Collection = Database['your collection Name']

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
    get_username = user_name.get()
    get_password = user_password.get()
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
            Clients_Collection.insert_one({'Username': get_username, 'Password': hash_password, 'Balance': 0.00, 'Privilege': 'user'})
            messagebox.showinfo(title='Success', message='Successfully Registered account!')
userForm()