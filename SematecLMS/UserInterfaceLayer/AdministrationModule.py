from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, DANGER, SECONDARY, Radiobutton, \
    IntVar, Combobox, SUCCESS
from tkinter import messagebox as msg, StringVar, HORIZONTAL
from tkinter.ttk import Labelframe, Treeview, Scrollbar, Checkbutton
from BusinessLogicLayer.Admin_CRUD_BLL import Admin_CRUD_BLL_Class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh
from .PersonPhotoPicker import PersonPhotoPicker


class AdministrationFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.admin_bll = Admin_CRUD_BLL_Class()
        self.people = {}
        self.person_options = {}
        self.filtered_people = []
        self.users = {}
        self.selected_user_id = None
        self.selected_user_person_id = None
        initialize_lazy_page(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.header = Label(self, text="Administration Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.administration_info = Labelframe(self, text="Administration Information",
                                              style=SUCCESS)
        self.administration_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.administration_info.grid_columnconfigure(0, weight=1)
        self.administration_info.grid_columnconfigure(1, weight=1)

        self.administration_list = Labelframe(self, text="Administration List", style=SUCCESS)
        self.administration_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.administration_list.grid_columnconfigure(0, weight=1)
        self.administration_list.grid_rowconfigure(0, weight=1)

        self.administration_tree_scroll_y = Scrollbar(self.administration_list)
        self.administration_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.administration_tree_scroll_x = Scrollbar(self.administration_list, orient=HORIZONTAL)
        self.administration_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.administration_tree = Treeview(self.administration_list,
                                            yscrollcommand=self.administration_tree_scroll_y.set,
                                            xscrollcommand=self.administration_tree_scroll_x.set, selectmode="extended",
                                            height=8)
        self.administration_tree.grid(row=0, column=0, sticky='nsew')
        self.administration_tree_scroll_y.config(command=self.administration_tree.yview)
        self.administration_tree_scroll_x.config(command=self.administration_tree.xview)
        self.configure_administration_tree()
        self.administration_tree.bind('<<TreeviewSelect>>', self.on_user_select)

        self.person_selection_frame = Labelframe(self.administration_info, text='Existing Person', style=INFO)
        self.person_selection_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 4), sticky='ew')
        self.person_selection_frame.grid_columnconfigure(1, weight=1)
        self.person_selection_frame.grid_columnconfigure(3, weight=1)

        lbl_person = Label(self.person_selection_frame, text='Existing Person : ', style=INFO,
                           font=('Arial', 10, 'bold'))
        lbl_person.grid(row=0, column=0, padx=8, pady=6, sticky='w')

        self.txt_person = StringVar()
        self.cmb_person = Combobox(self.person_selection_frame, textvariable=self.txt_person,
                                   state='readonly', width=30)
        self.cmb_person.grid(row=0, column=1, padx=8, pady=6, sticky='ew')
        self.cmb_person.bind('<<ComboboxSelected>>', self.on_person_select)

        lbl_person_filter = Label(self.person_selection_frame, text='Filter : ', style=INFO, font=('Arial', 10, 'bold'))
        lbl_person_filter.grid(row=0, column=2, padx=(12, 4), pady=6, sticky='w')

        self.txt_person_filter = StringVar()
        self.ent_person_filter = Entry(self.person_selection_frame, textvariable=self.txt_person_filter, width=32)
        self.ent_person_filter.grid(row=0, column=3, padx=4, pady=6, sticky='ew')
        self.ent_person_filter.bind('<KeyRelease>', self.filter_people)

        filter_button = Button(self.person_selection_frame, text='Filter', bootstyle=OUTLINE + INFO,
                               command=self.filter_people)
        filter_button.grid(row=0, column=4, padx=4, pady=6, sticky='ew')

        refresh_people_button = Button(self.person_selection_frame, text='Refresh', bootstyle=OUTLINE + SUCCESS,
                                       command=self.load_people)
        refresh_people_button.grid(row=0, column=5, padx=(4, 8), pady=6, sticky='ew')

        person_info_frame = Labelframe(self.administration_info, text='Person Information', style=INFO)
        person_info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        person_info_frame.grid_columnconfigure(0, weight=0)
        person_info_frame.grid_columnconfigure(1, weight=1, minsize=220)
        person_info_frame.grid_columnconfigure(2, weight=0)
        person_info_frame.grid_columnconfigure(3, weight=2, minsize=360)
        person_info_frame.grid_columnconfigure(4, weight=0)

        lbl_person_id = Label(person_info_frame, text='Person ID : ')
        lbl_person_id.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.lbl_person_id_value = Label(person_info_frame, text='', anchor='w')
        self.lbl_person_id_value.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        lbl_full_name = Label(person_info_frame, text='Full Name : ')
        lbl_full_name.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.lbl_full_name_value = Label(person_info_frame, text='',
                                         wraplength=340, justify='left', anchor='w')
        self.lbl_full_name_value.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        lbl_national_id = Label(person_info_frame, text='National ID : ')
        lbl_national_id.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.lbl_national_id_value = Label(person_info_frame, text='', anchor='w')
        self.lbl_national_id_value.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        lbl_mobile = Label(person_info_frame, text='Mobile : ')
        lbl_mobile.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.lbl_mobile_value = Label(person_info_frame, text='', anchor='w')
        self.lbl_mobile_value.grid(row=1, column=3, padx=10, pady=10, sticky='ew')

        lbl_email = Label(person_info_frame, text='Email : ')
        lbl_email.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.lbl_email_value = Label(person_info_frame, text='',
                                     wraplength=520, justify='left', anchor='w')
        self.lbl_email_value.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky='ew')

        lbl_gender = Label(person_info_frame, text='Gender : ')
        lbl_gender.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.lbl_gender_value = Label(person_info_frame, text='', anchor='w')
        self.lbl_gender_value.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        lbl_birthdate = Label(person_info_frame, text='Birth Date : ')
        lbl_birthdate.grid(row=3, column=2, padx=10, pady=10, sticky='w')

        self.lbl_birthdate_value = Label(person_info_frame, text='', anchor='w')
        self.lbl_birthdate_value.grid(row=3, column=3, padx=10, pady=10, sticky='ew')

        lbl_education = Label(person_info_frame, text='Education : ')
        lbl_education.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.lbl_education_value = Label(person_info_frame, text='',
                                         wraplength=220, justify='left', anchor='w')
        self.lbl_education_value.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        lbl_roles = Label(person_info_frame, text='Roles : ')
        lbl_roles.grid(row=4, column=2, padx=10, pady=10, sticky='w')

        self.lbl_roles_value = Label(person_info_frame, text='',
                                     wraplength=340, justify='left', anchor='w')
        self.lbl_roles_value.grid(row=4, column=3, padx=10, pady=10, sticky='ew')

        lbl_address = Label(person_info_frame, text='Address : ')
        lbl_address.grid(row=5, column=0, padx=10, pady=10, sticky='nw')

        self.lbl_address_value = Label(person_info_frame, text='',
                                       wraplength=560, justify='left', anchor='w')
        self.lbl_address_value.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky='ew')

        self.person_photo_preview = PersonPhotoPicker(person_info_frame, editable=False)
        self.person_photo_preview.grid(row=0, column=4, rowspan=6, padx=(12, 10), pady=10, sticky='n')

        user_access_frame = Labelframe(self.administration_info, text='User Access Details', style=INFO)
        user_access_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        user_access_frame.grid_columnconfigure(1, weight=1)
        user_access_frame.grid_columnconfigure(3, weight=1)
        user_access_frame.grid_columnconfigure(4, weight=0)

        lbl_username = Label(user_access_frame, text='Username : ')
        lbl_username.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.txt_username = StringVar()
        self.ent_username = Entry(user_access_frame, textvariable=self.txt_username, width=32)
        self.ent_username.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        generate_username_button = Button(user_access_frame, text='Generate', bootstyle=OUTLINE + INFO,
                                          command=self.generate_username)
        generate_username_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.show_password_var = IntVar(value=0)
        self.chk_show_password = Checkbutton(user_access_frame, text='Show',
                                             variable=self.show_password_var,
                                             command=self.toggle_password_visibility)
        self.chk_show_password.grid(row=2, column=4, padx=5, pady=5, sticky='w')

        lbl_password = Label(user_access_frame, text='Password : ')
        lbl_password.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.txt_password = StringVar()
        self.ent_password = Entry(user_access_frame, textvariable=self.txt_password, width=32, show='*')
        self.ent_password.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        lbl_confirm_password = Label(user_access_frame, text='Confirm Password : ')
        lbl_confirm_password.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        self.txt_confirm_password = StringVar()
        self.ent_confirm_password = Entry(user_access_frame, textvariable=self.txt_confirm_password, width=32, show='*')
        self.ent_confirm_password.grid(row=2, column=3, padx=10, pady=10, sticky='w')

        lbl_firstname = Label(user_access_frame, text='First Name : ')
        lbl_firstname.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.txt_firstname = StringVar()
        self.ent_firstname = Entry(user_access_frame, textvariable=self.txt_firstname, width=32)
        self.ent_firstname.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        lbl_lastname = Label(user_access_frame, text='Last Name : ')
        lbl_lastname.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.txt_lastname = StringVar()
        self.ent_lastname = Entry(user_access_frame, textvariable=self.txt_lastname, width=32)
        self.ent_lastname.grid(row=1, column=3, padx=10, pady=10, sticky='w')

        lbl_is_admin = Label(user_access_frame, text='Admin Rights : ')
        lbl_is_admin.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.int_is_admin_var = IntVar()
        self.int_is_admin_var.set(0)

        admin_rights_frame = Frame(user_access_frame)
        admin_rights_frame.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        rb_no_admin = Radiobutton(admin_rights_frame, text="No", variable=self.int_is_admin_var, value=0)
        rb_no_admin.grid(row=0, column=0, padx=(0, 12), sticky='w')

        rb_admin = Radiobutton(admin_rights_frame, text="Yes", variable=self.int_is_admin_var, value=1)
        rb_admin.grid(row=0, column=1, sticky='w')

        lbl_is_active = Label(user_access_frame, text='Account Status : ')
        lbl_is_active.grid(row=3, column=2, padx=10, pady=10, sticky='w')

        self.int_is_active_var = IntVar(value=1)
        self.chk_is_active = Checkbutton(user_access_frame, text='Active', variable=self.int_is_active_var)
        self.chk_is_active.grid(row=3, column=3, padx=10, pady=10, sticky='w')

        for child in person_info_frame.winfo_children():
            child.grid_configure(pady=4)

        for child in user_access_frame.winfo_children():
            child.grid_configure(pady=4)

        action_frame = Frame(self.administration_info)
        action_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 8), sticky='ew')

        for column_index in range(5):
            action_frame.grid_columnconfigure(column_index, weight=1)

        search_button = Button(action_frame, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=0, column=0, padx=(0, 6), pady=4, sticky='ew')

        register_button = Button(action_frame, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=0, column=1, padx=6, pady=4, sticky='ew')

        update_button = Button(action_frame, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=0, column=2, padx=6, pady=4, sticky='ew')

        delete_button = Button(action_frame, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=0, column=3, padx=6, pady=4, sticky='ew')

        clear_button = Button(action_frame, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=0, column=4, padx=(6, 0), pady=4, sticky='ew')

        apply_form_field_layout(self.person_selection_frame)
        apply_form_field_layout(user_access_frame)
        apply_readonly_value_style(
            self.lbl_person_id_value,
            self.lbl_full_name_value,
            self.lbl_national_id_value,
            self.lbl_mobile_value,
            self.lbl_email_value,
            self.lbl_gender_value,
            self.lbl_birthdate_value,
            self.lbl_education_value,
            self.lbl_roles_value,
            self.lbl_address_value
        )

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING,
                                  command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.update_existing_person_visibility()

        if not self.require_admin_access():
            self.main_view.switch('Main')
            return

        self.winfo_toplevel().fit_to_content(self, min_width=1130, min_height=720)
        schedule_page_refresh(self)

    def update_existing_person_visibility(self):
        if self.current_user_is_admin():
            self.person_selection_frame.grid()
            return

        self.person_selection_frame.grid_remove()
        self.txt_person_filter.set('')

    def current_user_is_admin(self):
        user = getattr(self.main_view, 'current_user', None)
        return bool(getattr(user, 'is_admin', False))

    def require_admin_access(self):
        if self.current_user_is_admin():
            return True

        msg.showwarning('Access Denied', 'Only admin users can use Administration.')
        return False

    def mark_stale(self):
        mark_page_stale(self)

    def refresh_page(self):
        self.apply_page_data(self.load_page_data(self.get_refresh_request()))

    def get_refresh_request(self):
        return {'keyword': self.txt_username.get().strip() or None}

    def load_page_data(self, request=None):
        request = request or {}
        return {
            'people': self.admin_bll.get_people(),
            'users': self.admin_bll.search_users(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_people(data['people'])
        self.fill_administration_tree(data['users'])

    def search(self):
        if not self.require_admin_access():
            return

        try:
            keyword = self.txt_username.get().strip() or None
            users = self.admin_bll.search_users(keyword)
            self.fill_administration_tree(users)
        except Exception as error:
            msg.showerror('Search Users Failed', str(error))

    def register(self):
        if not self.require_admin_access():
            return

        try:
            self.admin_bll.register_user(self.create_user_data())
            msg.showinfo('Register User', 'User registered successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid User Data', str(error))
        except Exception as error:
            msg.showerror('Register User Failed', str(error))

    def update(self):
        if not self.require_admin_access():
            return

        try:
            user_data = self.create_user_data()
            user_data['user_id'] = self.selected_user_id
            self.admin_bll.update_user(user_data)
            msg.showinfo('Update User', 'User updated successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid User Data', str(error))
        except Exception as error:
            msg.showerror('Update User Failed', str(error))

    def delete(self):
        if not self.require_admin_access():
            return

        try:
            if not self.selected_user_id:
                raise ValueError('Please select a user first.')

            confirm = msg.askyesno('Delete User', 'Are you sure you want to delete this user?')
            if not confirm:
                return

            self.admin_bll.delete_user(self.selected_user_id)
            msg.showinfo('Delete User', 'User deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Delete User', str(error))
        except Exception as error:
            msg.showerror('Delete User Failed', str(error))

    def configure_administration_tree(self):
        columns = ('id', 'username', 'person', 'is_admin', 'is_active')
        headings = {
            'id': 'ID',
            'username': 'Username',
            'person': 'Person',
            'is_admin': 'Admin',
            'is_active': 'Active'
        }

        self.administration_tree.configure(columns=columns, show='headings')
        for column in columns:
            self.administration_tree.heading(column, text=headings[column], anchor='w')
            self.administration_tree.column(column, width=120, anchor='w', stretch=False)

        self.administration_tree.column('id', width=90, anchor='w', stretch=False)
        self.administration_tree.column('username', width=240, anchor='w', stretch=False)
        self.administration_tree.column('person', width=500, anchor='w', stretch=False)

    def load_people(self):
        people = self.admin_bll.get_people()
        self.apply_people(people)

    def apply_people(self, people):
        self.people = {}
        self.person_options = {}
        self.filtered_people = []

        for person in people:
            person_id = person.ID
            self.people[person_id] = person

        self.txt_person_filter.set('')
        self.refresh_person_options(self.get_available_people())

    def refresh_person_options(self, people):
        self.person_options = {}
        self.filtered_people = list(people)

        for person in self.filtered_people:
            self.person_options[self.get_person_display_text(person)] = person.ID

        values = list(self.person_options.keys())
        self.cmb_person.configure(values=values)

        if self.txt_person.get() and self.txt_person.get() not in values:
            self.txt_person.set('')

    def get_available_people(self, include_person_id=None):
        if include_person_id is None:
            include_person_id = self.selected_user_person_id

        return [
            person for person in self.people.values()
            if not getattr(person, 'HasUser', False) or person.ID == include_person_id
        ]

    def get_person_display_text(self, person):
        full_name = f'{person.FirstName} {person.LastName}'.strip()
        return f'{person.ID} - {full_name}'

    def filter_people(self, event=None):
        keyword = self.txt_person_filter.get().strip().lower()
        if not keyword:
            self.refresh_person_options(self.get_available_people())
            return

        filtered_people = [
            person for person in self.get_available_people()
            if keyword in self.get_person_search_text(person)
        ]
        self.refresh_person_options(filtered_people)

    def get_person_search_text(self, person):
        values = (
            person.ID,
            person.FirstName,
            person.LastName,
            person.NationalCode,
            person.Mobile,
            person.EmailAddress,
            getattr(person, 'EducationTitle', ''),
            getattr(person, 'Roles', '')
        )
        return ' '.join(str(value or '') for value in values).lower()

    def fill_administration_tree(self, users):
        self.users = {}
        for item_id in self.administration_tree.get_children():
            self.administration_tree.delete(item_id)

        for user in users:
            person_name = getattr(user, 'PersonName', '') or f'{user.FirstName} {user.LastName}'.strip()

            item_id = self.administration_tree.insert('', 'end', values=(
                user.ID,
                user.UserName,
                person_name,
                'Yes' if user.isAdmin else 'No',
                'Yes' if user.isActive else 'No'
            ))
            self.users[item_id] = user

    def on_person_select(self, event=None):
        selected_person_id = self.person_options.get(self.txt_person.get())
        person = self.people.get(selected_person_id)
        if not person:
            return

        self.fill_person_details(person, copy_names=True)

    def fill_person_details(self, person, copy_names=False):
        self.lbl_person_id_value.configure(text=person.ID)
        self.lbl_full_name_value.configure(text=f'{person.FirstName} {person.LastName}')
        self.lbl_national_id_value.configure(text=person.NationalCode or '')
        self.lbl_mobile_value.configure(text=person.Mobile or '')
        self.lbl_email_value.configure(text=person.EmailAddress or '')
        self.lbl_gender_value.configure(text=person.Gender or '')
        self.lbl_birthdate_value.configure(text=person.Birthdate or '')
        self.lbl_education_value.configure(text=getattr(person, 'EducationTitle', '') or '')
        self.lbl_roles_value.configure(text=getattr(person, 'Roles', '') or 'Person')
        self.lbl_address_value.configure(text=person.Address or '')
        self.person_photo_preview.set_database_photo(self.admin_bll.get_person_photo(person.ID))

        if copy_names:
            self.txt_firstname.set(person.FirstName)
            self.txt_lastname.set(person.LastName)

        if copy_names and not self.txt_username.get().strip():
            self.generate_username(show_warning=False)

    def clear_person_details(self):
        self.lbl_person_id_value.configure(text='')
        self.lbl_full_name_value.configure(text='')
        self.lbl_national_id_value.configure(text='')
        self.lbl_mobile_value.configure(text='')
        self.lbl_email_value.configure(text='')
        self.lbl_gender_value.configure(text='')
        self.lbl_birthdate_value.configure(text='')
        self.lbl_education_value.configure(text='')
        self.lbl_roles_value.configure(text='')
        self.lbl_address_value.configure(text='')
        self.person_photo_preview.clear()

    def select_person_by_id(self, person_id):
        self.txt_person_filter.set('')
        self.refresh_person_options(self.get_available_people(person_id))

        if not person_id:
            self.txt_person.set('')
            self.clear_person_details()
            return

        person = self.people.get(person_id)
        if not person:
            self.txt_person.set('')
            self.clear_person_details()
            return

        self.txt_person.set(self.get_person_display_text(person))
        self.fill_person_details(person, copy_names=False)

    def on_user_select(self, event=None):
        selected_item_ids = self.administration_tree.selection()
        if not selected_item_ids:
            return

        user = self.users.get(selected_item_ids[0])
        if not user:
            return

        self.selected_user_id = user.ID
        self.selected_user_person_id = getattr(user, 'PersonID', None)
        self.select_person_by_id(self.selected_user_person_id)
        self.txt_username.set(user.UserName)
        self.txt_password.set('')
        self.txt_confirm_password.set('')
        self.txt_firstname.set(user.FirstName)
        self.txt_lastname.set(user.LastName)
        self.int_is_admin_var.set(1 if user.isAdmin else 0)
        self.int_is_active_var.set(1 if user.isActive else 0)

    def create_user_data(self):
        return {
            'username': self.txt_username.get().strip(),
            'password': self.txt_password.get().strip(),
            'confirm_password': self.txt_confirm_password.get().strip(),
            'firstname': self.txt_firstname.get().strip(),
            'lastname': self.txt_lastname.get().strip(),
            'is_admin': self.int_is_admin_var.get(),
            'is_active': self.int_is_active_var.get(),
            'person_id': self.person_options.get(self.txt_person.get())
        }

    def generate_username(self, show_warning=True):
        first_name = self.txt_firstname.get().strip()
        last_name = self.txt_lastname.get().strip()
        username = self.normalize_username(f'{first_name}.{last_name}')

        if not username:
            selected_person_id = self.person_options.get(self.txt_person.get())
            person = self.people.get(selected_person_id)
            if person:
                username = self.normalize_username(f'{person.FirstName}.{person.LastName}')

        if not username:
            if show_warning:
                msg.showwarning('Generate Username', 'First name and last name are required.')
            return

        self.txt_username.set(username[:50])

    def normalize_username(self, value):
        cleaned_value = value.lower().replace(' ', '.')
        allowed_value = ''.join(
            character for character in cleaned_value
            if character.isascii() and (character.isalnum() or character in '._')
        )
        return '.'.join(part for part in allowed_value.split('.') if part)

    def clear_form(self):
        self.selected_user_id = None
        self.selected_user_person_id = None
        self.txt_person.set('')
        self.txt_person_filter.set('')
        self.txt_username.set('')
        self.txt_password.set('')
        self.txt_confirm_password.set('')
        self.txt_firstname.set('')
        self.txt_lastname.set('')
        self.int_is_admin_var.set(0)
        self.int_is_active_var.set(1)
        self.show_password_var.set(0)
        self.ent_password.configure(show='*')
        self.ent_confirm_password.configure(show='*')
        self.clear_person_details()
        self.refresh_person_options(self.get_available_people())

        for item_id in self.administration_tree.selection():
            self.administration_tree.selection_remove(item_id)

    def toggle_password_visibility(self):
        show_value = '' if self.show_password_var.get() else '*'
        self.ent_password.configure(show=show_value)
        self.ent_confirm_password.configure(show=show_value)
