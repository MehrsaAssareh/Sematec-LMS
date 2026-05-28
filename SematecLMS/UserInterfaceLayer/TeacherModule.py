from datetime import datetime
from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, SUCCESS, DANGER, SECONDARY, \
    Radiobutton, DateEntry, IntVar, Combobox
from tkinter import messagebox as msg, StringVar, HORIZONTAL
from tkinter.ttk import Labelframe, Treeview, Scrollbar
from BusinessLogicLayer.Teacher_CRUD_BLL import Teacher_CRUD_BLL_Class
from Model.TeacherModel import Teacher_Model_Class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh
from .PersonPhotoPicker import PersonPhotoPicker


class TeacherFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.teacher_bll = Teacher_CRUD_BLL_Class()
        self.selected_person_id = None
        self.education_options = {}
        self.existing_people = {}
        self.existing_person_options = {}
        self.teacher_rows = {}
        initialize_lazy_page(self)
        self.selected_existing_person_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.header_bar = Frame(self)
        self.header_bar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.header_bar.grid_columnconfigure(0, weight=1)

        self.header = Label(self.header_bar, text="Teacher Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=0, column=0, sticky="w")

        self.existing_person_frame = Frame(self.header_bar)
        self.existing_person_frame.grid(row=0, column=1, sticky='e')
        Label(self.existing_person_frame, text='Existing Person: ').grid(row=0, column=0, padx=(0, 4), sticky='w')
        self.txt_existing_person = StringVar()
        self.cmb_existing_person = Combobox(
            self.existing_person_frame,
            textvariable=self.txt_existing_person,
            state='readonly',
            width=34
        )
        self.cmb_existing_person.grid(row=0, column=1, sticky='ew')
        self.cmb_existing_person.bind('<<ComboboxSelected>>', self.on_existing_person_select)

        self.teacher_info = Labelframe(self, text="Teacher Information", style=SUCCESS)
        self.teacher_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.teacher_info.grid_columnconfigure(0, weight=0)
        self.teacher_info.grid_columnconfigure(1, weight=1)
        self.teacher_info.grid_columnconfigure(2, weight=0)
        self.teacher_info.grid_columnconfigure(3, weight=1)

        self.teacher_list = Labelframe(self, text="Teacher List", style=SUCCESS)
        self.teacher_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.teacher_list.grid_columnconfigure(0, weight=1)
        self.teacher_list.grid_rowconfigure(0, weight=1)

        self.teacher_tree_scroll_y = Scrollbar(self.teacher_list)
        self.teacher_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.teacher_tree_scroll_x = Scrollbar(self.teacher_list, orient=HORIZONTAL)
        self.teacher_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.teacher_tree = Treeview(self.teacher_list, yscrollcommand=self.teacher_tree_scroll_y.set,
                                     xscrollcommand=self.teacher_tree_scroll_x.set, selectmode="extended", height=8)
        self.teacher_tree.grid(row=0, column=0, sticky='nsew')
        self.teacher_tree_scroll_y.config(command=self.teacher_tree.yview)
        self.teacher_tree_scroll_x.config(command=self.teacher_tree.xview)
        self.configure_teacher_tree()
        self.teacher_tree.bind('<<TreeviewSelect>>', self.on_teacher_select)

        lbl_firstname = Label(self.teacher_info, text='Firstname: ')
        lbl_firstname.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_firstname = StringVar()
        self.ent_firstname = Entry(self.teacher_info, textvariable=self.txt_firstname, width=32)
        self.ent_firstname.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        lbl_lastname = Label(self.teacher_info, text='Lastname: ')
        lbl_lastname.grid(row=0, column=2, padx=10, pady=6, sticky='w')
        self.txt_lastname = StringVar()
        self.ent_lastname = Entry(self.teacher_info, textvariable=self.txt_lastname, width=32)
        self.ent_lastname.grid(row=0, column=3, padx=10, pady=6, sticky='w')

        lbl_birthdate = Label(self.teacher_info, text='Birth Date: ')
        lbl_birthdate.grid(row=1, column=0, padx=10, pady=6, sticky='w')
        self.ent_birthdate = DateEntry(self.teacher_info, width=27)
        self.ent_birthdate.grid(row=1, column=1, padx=10, pady=6, sticky='w')

        lbl_national_code = Label(self.teacher_info, text='National ID: ')
        lbl_national_code.grid(row=1, column=2, padx=10, pady=6, sticky='w')
        self.txt_national_code = StringVar()
        self.ent_national_code = Entry(self.teacher_info, textvariable=self.txt_national_code, width=32)
        self.ent_national_code.grid(row=1, column=3, padx=10, pady=6, sticky='w')

        lbl_gender = Label(self.teacher_info, text='Gender: ')
        lbl_gender.grid(row=2, column=0, padx=10, pady=6, sticky='w')
        self.txt_gender = IntVar(value=1)
        gender_frame = Frame(self.teacher_info)
        gender_frame.grid(row=2, column=1, padx=10, pady=6, sticky='w')
        rb_male = Radiobutton(gender_frame, text="Male", variable=self.txt_gender, value=1)
        rb_female = Radiobutton(gender_frame, text="Female", variable=self.txt_gender, value=0)
        rb_male.grid(row=0, column=0, padx=(0, 12), sticky='w')
        rb_female.grid(row=0, column=1, sticky='w')

        lbl_marital_status = Label(self.teacher_info, text='Marital Status: ')
        lbl_marital_status.grid(row=2, column=2, padx=10, pady=6, sticky='w')
        self.int_marital_status_var = IntVar(value=0)
        marital_status_frame = Frame(self.teacher_info)
        marital_status_frame.grid(row=2, column=3, padx=10, pady=6, sticky='w')
        rb_single = Radiobutton(marital_status_frame, text="Single", variable=self.int_marital_status_var, value=0)
        rb_married = Radiobutton(marital_status_frame, text="Married", variable=self.int_marital_status_var, value=1)
        rb_single.grid(row=0, column=0, padx=(0, 12), sticky='w')
        rb_married.grid(row=0, column=1, sticky='w')

        lbl_mobile = Label(self.teacher_info, text='Mobile No.: ')
        lbl_mobile.grid(row=3, column=0, padx=10, pady=6, sticky='w')
        self.txt_mobile = StringVar()
        self.ent_mobile = Entry(self.teacher_info, textvariable=self.txt_mobile, width=32)
        self.ent_mobile.grid(row=3, column=1, padx=10, pady=6, sticky='w')

        lbl_email_address = Label(self.teacher_info, text='Email Address: ')
        lbl_email_address.grid(row=3, column=2, padx=10, pady=6, sticky='w')
        self.txt_email_address = StringVar()
        self.ent_email_address = Entry(self.teacher_info, textvariable=self.txt_email_address, width=32)
        self.ent_email_address.grid(row=3, column=3, padx=10, pady=6, sticky='w')

        lbl_address = Label(self.teacher_info, text='Address: ')
        lbl_address.grid(row=4, column=0, padx=10, pady=6, sticky='w')
        self.txt_address = StringVar()
        self.ent_address = Entry(self.teacher_info, textvariable=self.txt_address, width=32)
        self.ent_address.grid(row=4, column=1, padx=10, pady=6, sticky='w')

        lbl_education = Label(self.teacher_info, text='Education: ')
        lbl_education.grid(row=4, column=2, padx=10, pady=6, sticky='w')
        self.txt_education = StringVar()
        self.cmb_education = Combobox(self.teacher_info, textvariable=self.txt_education, state='readonly', width=30)
        self.cmb_education.grid(row=4, column=3, padx=10, pady=6, sticky='w')

        lbl_insurance_number = Label(self.teacher_info, text='Insurance No.: ')
        lbl_insurance_number.grid(row=5, column=0, padx=10, pady=6, sticky='w')
        self.txt_insurance_number = StringVar()
        self.ent_insurance_number = Entry(self.teacher_info, textvariable=self.txt_insurance_number, width=32)
        self.ent_insurance_number.grid(row=5, column=1, padx=10, pady=6, sticky='w')

        lbl_account_number = Label(self.teacher_info, text='Account No.: ')
        lbl_account_number.grid(row=5, column=2, padx=10, pady=6, sticky='w')
        self.txt_account_number = StringVar()
        self.ent_account_number = Entry(self.teacher_info, textvariable=self.txt_account_number, width=32)
        self.ent_account_number.grid(row=5, column=3, padx=10, pady=6, sticky='w')

        lbl_start_date = Label(self.teacher_info, text='Start Date: ')
        lbl_start_date.grid(row=6, column=0, padx=10, pady=6, sticky='w')
        self.ent_start_date = DateEntry(self.teacher_info, width=27)
        self.ent_start_date.grid(row=6, column=1, padx=10, pady=6, sticky='w')

        lbl_teacher_id = Label(self.teacher_info, text='Teacher ID: ')
        lbl_teacher_id.grid(row=6, column=2, padx=10, pady=6, sticky='w')
        self.lbl_teacher_id_value = Label(self.teacher_info, text='')
        self.lbl_teacher_id_value.grid(row=6, column=3, padx=10, pady=6, sticky='w')

        lbl_search_keyword = Label(self.teacher_info, text='Search Keyword: ')
        lbl_search_keyword.grid(row=7, column=0, padx=10, pady=6, sticky='w')
        self.txt_search_keyword = StringVar()
        self.ent_search_keyword = Entry(self.teacher_info, textvariable=self.txt_search_keyword, width=32)
        self.ent_search_keyword.grid(row=7, column=1, padx=10, pady=6, sticky='w')

        lbl_photo = Label(self.teacher_info, text='Photo: ')
        lbl_photo.grid(row=7, column=2, padx=10, pady=6, sticky='nw')
        self.photo_picker = PersonPhotoPicker(self.teacher_info)
        self.photo_picker.grid(row=7, column=3, rowspan=2, padx=10, pady=6, sticky='w')

        search_button = Button(self.teacher_info, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=9, column=0, padx=10, pady=12, sticky='ew')

        register_button = Button(self.teacher_info, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=9, column=1, padx=10, pady=12, sticky='ew')

        update_button = Button(self.teacher_info, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=9, column=2, padx=10, pady=12, sticky='ew')

        delete_button = Button(self.teacher_info, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=9, column=3, padx=10, pady=12, sticky='ew')

        clear_button = Button(self.teacher_info, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=10, column=0, columnspan=4, padx=10, pady=(0, 12), sticky='ew')

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING, command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        apply_form_field_layout(self.teacher_info)
        apply_readonly_value_style(self.lbl_teacher_id_value)

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.update_existing_person_visibility()
        self.winfo_toplevel().fit_to_content(self, min_width=940, min_height=900)
        schedule_page_refresh(self)

    def update_existing_person_visibility(self):
        if self.current_user_is_admin():
            self.existing_person_frame.grid()
            return

        self.existing_person_frame.grid_remove()
        self.selected_existing_person_id = None
        self.txt_existing_person.set('')

    def current_user_is_admin(self):
        user = getattr(self.main_view, 'current_user', None)
        return bool(getattr(user, 'is_admin', False))

    def mark_stale(self):
        mark_page_stale(self)

    def refresh_page(self):
        self.apply_page_data(self.load_page_data(self.get_refresh_request()))

    def get_refresh_request(self):
        return {'keyword': self.get_search_keyword()}

    def load_page_data(self, request=None):
        request = request or {}
        return {
            'lookups': self.teacher_bll.get_form_lookups(),
            'teachers': self.teacher_bll.search_teachers(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_form_lookups(data['lookups'])
        self.fill_teacher_tree(data['teachers'])

    def search(self):
        refresh_page_now(self)

    def register(self):
        try:
            self.teacher_bll.register_teacher(self.create_teacher_model(self.selected_existing_person_id))
            msg.showinfo('Register Teacher', 'Teacher registered successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Teacher Data', str(error))
        except Exception as error:
            msg.showerror('Register Teacher Failed', str(error))

    def update(self):
        try:
            teacher = self.create_teacher_model(self.selected_person_id)
            self.teacher_bll.update_teacher(teacher)
            msg.showinfo('Update Teacher', 'Teacher updated successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Teacher Data', str(error))
        except Exception as error:
            msg.showerror('Update Teacher Failed', str(error))

    def delete(self):
        try:
            if not self.selected_person_id:
                raise ValueError('Please select a teacher first.')

            confirm = msg.askyesno('Delete Teacher', 'Are you sure you want to delete this teacher?')
            if not confirm:
                return

            self.teacher_bll.delete_teacher(self.selected_person_id)
            msg.showinfo('Delete Teacher', 'Teacher deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Delete Teacher', str(error))
        except Exception as error:
            msg.showerror('Delete Teacher Failed', str(error))

    def create_teacher_model(self, person_id=None):
        return Teacher_Model_Class(
            person_id=person_id,
            firstname=self.get_required_text(self.txt_firstname, 'Firstname'),
            lastname=self.get_required_text(self.txt_lastname, 'Lastname'),
            birthdate=self.get_required_date(self.ent_birthdate, 'Birth Date'),
            marital_status=self.get_marital_status_text(),
            national_code=self.get_required_text(self.txt_national_code, 'National ID'),
            mobile=self.get_required_text(self.txt_mobile, 'Mobile No.'),
            address=self.get_optional_text(self.txt_address),
            gender=self.get_gender_text(),
            education_id=self.get_required_lookup_id(self.txt_education, self.education_options, 'Education'),
            email_address=self.get_optional_text(self.txt_email_address),
            insurance_number=self.get_required_text(self.txt_insurance_number, 'Insurance No.'),
            account_number=self.get_required_text(self.txt_account_number, 'Account No.'),
            start_date=self.get_required_date(self.ent_start_date, 'Start Date'),
            **self.photo_picker.get_change()
        )

    def clear_form(self):
        self.selected_person_id = None
        self.selected_existing_person_id = None
        self.txt_existing_person.set('')
        for variable in (
                self.txt_firstname, self.txt_lastname, self.txt_national_code, self.txt_mobile,
                self.txt_email_address, self.txt_address, self.txt_education,
                self.txt_insurance_number, self.txt_account_number):
            variable.set('')

        self.ent_birthdate.entry.delete(0, 'end')
        self.ent_start_date.entry.delete(0, 'end')
        self.txt_gender.set(1)
        self.int_marital_status_var.set(0)
        self.txt_search_keyword.set('')
        self.lbl_teacher_id_value.configure(text='')
        self.photo_picker.clear()

        for item_id in self.teacher_tree.selection():
            self.teacher_tree.selection_remove(item_id)

    def get_required_text(self, variable, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')
        return value

    def get_optional_text(self, variable):
        value = variable.get().strip()
        return value if value else None

    def get_required_lookup_id(self, variable, options, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        if value not in options:
            raise ValueError(f'Please choose a valid {field_name}.')

        return options[value]

    def get_required_date(self, date_entry, field_name):
        value = date_entry.entry.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        for date_format in ('%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y'):
            try:
                return datetime.strptime(value, date_format).date()
            except ValueError:
                pass

        raise ValueError(f'{field_name} must be a valid date.')

    def get_gender_text(self):
        return 'Male' if self.txt_gender.get() == 1 else 'Female'

    def get_marital_status_text(self):
        return 'Married' if self.int_marital_status_var.get() == 1 else 'Single'

    def get_search_keyword(self):
        search_keyword = self.txt_search_keyword.get().strip()
        if search_keyword:
            return search_keyword

        values = [
            self.txt_firstname.get().strip(),
            self.txt_lastname.get().strip(),
            self.txt_national_code.get().strip(),
            self.txt_mobile.get().strip(),
            self.txt_insurance_number.get().strip(),
            self.txt_account_number.get().strip()
        ]

        for value in values:
            if value:
                return value

        return None

    def configure_teacher_tree(self):
        self.teacher_columns = (
            'person_id', 'full_name', 'mobile', 'education', 'start_date'
        )
        headings = {
            'person_id': 'Person ID',
            'full_name': 'Teacher Name',
            'mobile': 'Mobile',
            'education': 'Education',
            'start_date': 'Start Date'
        }

        self.teacher_tree.configure(columns=self.teacher_columns, show='headings')
        for column in self.teacher_columns:
            self.teacher_tree.heading(column, text=headings[column], anchor='w')
            self.teacher_tree.column(column, width=120, anchor='w', stretch=False)

        self.teacher_tree.column('full_name', width=300, anchor='w', stretch=False)
        self.teacher_tree.column('mobile', width=150, anchor='w', stretch=False)
        self.teacher_tree.column('education', width=150, anchor='w', stretch=False)
        self.teacher_tree.column('start_date', width=130, anchor='w', stretch=False)

    def fill_teacher_tree(self, teachers):
        self.teacher_rows = {}
        for item_id in self.teacher_tree.get_children():
            self.teacher_tree.delete(item_id)

        for teacher in teachers:
            item_id = self.teacher_tree.insert('', 'end', values=(
                teacher.person_id,
                f'{teacher.firstname} {teacher.lastname}'.strip(),
                teacher.mobile,
                self.get_lookup_display_text(self.education_options, teacher.education_id),
                teacher.start_date
            ))
            self.teacher_rows[item_id] = teacher

    def on_teacher_select(self, event=None):
        selected_item_ids = self.teacher_tree.selection()
        if not selected_item_ids:
            return

        teacher = self.teacher_rows.get(selected_item_ids[0])
        if not teacher:
            return

        self.selected_person_id = teacher.person_id
        self.selected_existing_person_id = None
        self.txt_existing_person.set('')
        self.lbl_teacher_id_value.configure(text=teacher.person_id)
        self.txt_firstname.set(teacher.firstname)
        self.txt_lastname.set(teacher.lastname)
        self.set_date_entry_text(self.ent_birthdate, teacher.birthdate)
        self.int_marital_status_var.set(1 if teacher.marital_status == 'Married' else 0)
        self.txt_national_code.set(teacher.national_code)
        self.txt_mobile.set(teacher.mobile)
        self.txt_address.set(teacher.address or '')
        self.txt_gender.set(1 if teacher.gender == 'Male' else 0)
        self.txt_email_address.set(teacher.email_address or '')
        self.set_lookup_value(self.txt_education, self.education_options, teacher.education_id)
        self.txt_insurance_number.set(teacher.insurance_number)
        self.txt_account_number.set(teacher.account_number)
        self.set_date_entry_text(self.ent_start_date, teacher.start_date)
        self.photo_picker.set_database_photo(self.teacher_bll.get_person_photo(teacher.person_id))

    def set_date_entry_text(self, date_entry, value):
        date_entry.entry.delete(0, 'end')
        if value:
            date_entry.entry.insert(0, value)

    def load_form_lookups(self):
        try:
            self.apply_form_lookups(self.teacher_bll.get_form_lookups())
        except Exception as error:
            msg.showerror('Teacher Form Setup Failed', str(error))

    def apply_form_lookups(self, lookups):
        self.education_options = self.build_lookup_options(lookups['education'])
        self.cmb_education.configure(values=list(self.education_options.keys()))
        self.existing_people = {
            person['person_id']: person
            for person in lookups.get('available_people', [])
        }
        self.existing_person_options = {
            self.get_existing_person_display_text(person): person['person_id']
            for person in lookups.get('available_people', [])
        }
        self.cmb_existing_person.configure(values=list(self.existing_person_options.keys()))

        if self.txt_existing_person.get() and self.txt_existing_person.get() not in self.existing_person_options:
            self.txt_existing_person.set('')
            self.selected_existing_person_id = None

    def get_existing_person_display_text(self, person):
        full_name = f"{person['firstname']} {person['lastname']}".strip()
        return f"{person['person_id']} - {full_name}"

    def on_existing_person_select(self, event=None):
        person_id = self.existing_person_options.get(self.txt_existing_person.get())
        person = self.existing_people.get(person_id)
        if not person:
            return

        self.selected_existing_person_id = person_id
        self.selected_person_id = None
        self.lbl_teacher_id_value.configure(text='')
        self.txt_firstname.set(person['firstname'] or '')
        self.txt_lastname.set(person['lastname'] or '')
        self.set_date_entry_text(self.ent_birthdate, person['birthdate'])
        self.int_marital_status_var.set(1 if person['marital_status'] == 'Married' else 0)
        self.txt_national_code.set(person['national_code'] or '')
        self.txt_mobile.set(person['mobile'] or '')
        self.txt_address.set(person['address'] or '')
        self.txt_gender.set(1 if person['gender'] == 'Male' else 0)
        self.txt_email_address.set(person['email_address'] or '')
        self.set_lookup_value(self.txt_education, self.education_options, person['education_id'])
        self.photo_picker.set_database_photo(self.teacher_bll.get_person_photo(person_id))

    def build_lookup_options(self, rows):
        options = {}
        for row_id, title in rows:
            display_text = f'{row_id} - {title}'
            options[display_text] = row_id

        return options

    def set_lookup_value(self, variable, options, selected_id):
        if selected_id in ('', None):
            variable.set('')
            return

        try:
            selected_id = int(selected_id)
        except ValueError:
            variable.set('')
            return

        for display_text, option_id in options.items():
            if option_id == selected_id:
                variable.set(display_text)
                return

        variable.set('')

    def get_lookup_display_text(self, options, selected_id):
        if selected_id in ('', None):
            return ''

        try:
            selected_id = int(selected_id)
        except ValueError:
            return ''

        for display_text, option_id in options.items():
            if option_id == selected_id:
                return display_text

        return str(selected_id)
