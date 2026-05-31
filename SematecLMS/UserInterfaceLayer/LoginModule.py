import os
from ttkbootstrap import Frame, Label, Entry, Button, END, SUCCESS, INFO, OUTLINE, PRIMARY
from tkinter import messagebox as msg, StringVar, PhotoImage
from BusinessLogicLayer.Login_CRUD_BLL import Login_CRUD_BLL_Class
from .FormLayout import apply_form_field_layout


class LoginFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.login_bll = Login_CRUD_BLL_Class()
        self.password_show_icon = None
        self.password_hide_icon = None
        self.load_password_toggle_icons()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_form = Frame(self)
        self.login_form.grid(row=0, column=0, padx=32, pady=32)
        self.login_form.grid_columnconfigure(1, weight=1)
        self.login_form.grid_columnconfigure(2, weight=0)

        self.welcome_header = Label(
            self.login_form,
            text="Welcome to Sematec Learning Management System!",
            style=SUCCESS,
            font=('Arial', 16, 'bold')
        )
        self.welcome_header.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.header = Label(self.login_form, text="Login Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        self.lbl_username = Label(self.login_form, text="Username :", style=PRIMARY)
        self.lbl_username.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="w")

        self.txt_username = StringVar()
        self.ent_username = Entry(self.login_form, textvariable=self.txt_username, width=32)
        self.ent_username.grid(row=2, column=1, columnspan=2, pady=(0, 10), padx=(0, 10), sticky="ew")

        self.lbl_password = Label(self.login_form, text="Password :", style=PRIMARY)
        self.lbl_password.grid(row=3, column=0, pady=(0, 10), padx=10, sticky="w")

        self.txt_password = StringVar()
        self.ent_password = Entry(self.login_form, show="*", textvariable=self.txt_password, width=32)
        self.ent_password.grid(row=3, column=1, pady=(0, 10), padx=(0, 6), sticky="ew")

        self.btn_login = Button(self.login_form, text="Login", bootstyle=SUCCESS, command=self.login)
        self.btn_login.grid(row=4, column=1, columnspan=2, pady=(8, 0), padx=(0, 10), sticky="ew")

        self.btn_show_hide = Button(
            self.login_form,
            bootstyle=OUTLINE + PRIMARY,
            width=4,
            command=self.show_hide_command,
            takefocus=False
        )
        self.set_password_toggle_button(is_password_visible=False)
        self.btn_show_hide.grid(row=3, column=2, padx=(0, 10), pady=(0, 10), sticky='ew')

        apply_form_field_layout(self.login_form)

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self, min_width=520, min_height=300)

    def login(self):
        username = self.txt_username.get()
        password = self.txt_password.get()

        user_model = self.login_bll.login_user(username, password)

        if user_model:
            msg.showinfo('Login Successful!', f'Welcome {user_model.firstname}!')
            self.main_view.set_current_user(user_model)
            self.main_view.switch('Main')
            self.ent_username.delete(0, END)
            self.ent_password.delete(0, END)
        else:
            msg.showerror('Login Failed!', 'Username or Password is incorrect!')
            self.ent_username.delete(0, END)
            self.ent_password.delete(0, END)

    def show_hide_command(self):
        if self.ent_password.cget('show') == '*':
            self.ent_password.config(show='')
            self.set_password_toggle_button(is_password_visible=True)
        else:
            self.ent_password.config(show='*')
            self.set_password_toggle_button(is_password_visible=False)

    def load_password_toggle_icons(self):
        icon_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'images', 'password_icons')
        )
        show_icon_path = os.path.join(icon_folder, 'eye_24.png')
        hide_icon_path = os.path.join(icon_folder, 'eye_off_24.png')

        if os.path.exists(show_icon_path) and os.path.exists(hide_icon_path):
            self.password_show_icon = PhotoImage(file=show_icon_path)
            self.password_hide_icon = PhotoImage(file=hide_icon_path)

    def set_password_toggle_button(self, is_password_visible):
        if self.password_show_icon and self.password_hide_icon:
            icon = self.password_hide_icon if is_password_visible else self.password_show_icon
            self.btn_show_hide.configure(image=icon, text='', compound='center')
            return

        self.btn_show_hide.configure(text='Hide' if is_password_visible else 'Show', image='')
