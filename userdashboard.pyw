import customtkinter
from pymongo import *

Client = MongoClient('connection string')
Database = Client['Database Name']
Clients_Collection = Database['Collection name']

def userForm():
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

    not_usr_btn = customtkinter.CTkButton(master=panel, width=65, height=15, text="Sign Up", fg_color='#242424', bg_color='#242424', corner_radius=0, border_width=0,hover_color='#242424')
    not_usr_btn.place(x=105, y=168)

    separator = customtkinter.CTkFrame(master=panel, width=300, height=4, corner_radius=0, fg_color='#FFFFFF')
    separator.place(x=25, y=205)
    root.mainloop()
userForm()