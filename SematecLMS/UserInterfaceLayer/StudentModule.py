from datetime import datetime
from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, SUCCESS, DANGER, SECONDARY, \
    Radiobutton, DateEntry, IntVar, Combobox
from tkinter import messagebox as msg, StringVar, HORIZONTAL
from tkinter.ttk import Labelframe, Treeview, Scrollbar
from BusinessLogicLayer.Student_CRUD_BLL import Student_CRUD_BLL_Class
from Model.StudentModel import Student_Model_Class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh
from .PersonPhotoPicker import PersonPhotoPicker


class StudentFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.student_bll = Student_CRUD_BLL_Class()
        self.selected_person_id = None
        self.education_options = {}
        self.existing_people = {}
        self.existing_person_options = {}
        self.student_rows = {}
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

        self.header = Label(self.header_bar, text="Student Page", style=PRIMARY, font=('Arial', 15, 'bold'))
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

        self.student_info = Labelframe(self, text="Student Information", style=SUCCESS)
        self.student_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.student_info.grid_columnconfigure(0, weight=0)
        self.student_info.grid_columnconfigure(1, weight=1)
        self.student_info.grid_columnconfigure(2, weight=0)
        self.student_info.grid_columnconfigure(3, weight=1)

        self.student_list = Labelframe(self, text="Student List", style=SUCCESS)
        self.student_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.student_list.grid_columnconfigure(0, weight=1)
        self.student_list.grid_rowconfigure(0, weight=1)

        self.student_tree_scroll_y = Scrollbar(self.student_list)
        self.student_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.student_tree_scroll_x = Scrollbar(self.student_list, orient=HORIZONTAL)
        self.student_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.student_tree = Treeview(self.student_list, yscrollcommand=self.student_tree_scroll_y.set,
                                     xscrollcommand=self.student_tree_scroll_x.set, selectmode="extended", height=8)
        self.student_tree.grid(row=0, column=0, sticky='nsew')
        self.student_tree_scroll_y.config(command=self.student_tree.yview)
        self.student_tree_scroll_x.config(command=self.student_tree.xview)
        self.configure_student_tree()
        self.student_tree.bind('<<TreeviewSelect>>', self.on_student_select)

        lbl_firstname = Label(self.student_info, text='Firstname: ')
        lbl_firstname.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_firstname = StringVar()
        self.ent_firstname = Entry(self.student_info, textvariable=self.txt_firstname, width=32)
        self.ent_firstname.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        lbl_lastname = Label(self.student_info, text='Lastname: ')
        lbl_lastname.grid(row=0, column=2, padx=10, pady=6, sticky='w')
        self.txt_lastname = StringVar()
        self.ent_lastname = Entry(self.student_info, textvariable=self.txt_lastname, width=32)
        self.ent_lastname.grid(row=0, column=3, padx=10, pady=6, sticky='w')

        lbl_birthdate = Label(self.student_info, text='Birth Date: ')
        lbl_birthdate.grid(row=1, column=0, padx=10, pady=6, sticky='w')
        self.ent_birthdate = DateEntry(self.student_info, width=27)
        self.ent_birthdate.grid(row=1, column=1, padx=10, pady=6, sticky='w')

        lbl_national_code = Label(self.student_info, text='National ID: ')
        lbl_national_code.grid(row=1, column=2, padx=10, pady=6, sticky='w')
        self.txt_national_code = StringVar()
        self.ent_national_code = Entry(self.student_info, textvariable=self.txt_national_code, width=32)
        self.ent_national_code.grid(row=1, column=3, padx=10, pady=6, sticky='w')

        lbl_gender = Label(self.student_info, text='Gender: ')
        lbl_gender.grid(row=2, column=0, padx=10, pady=6, sticky='w')
        self.txt_gender = IntVar(value=1)
        gender_frame = Frame(self.student_info)
        gender_frame.grid(row=2, column=1, padx=10, pady=6, sticky='w')
        rb_male = Radiobutton(gender_frame, text="Male", variable=self.txt_gender, value=1)
        rb_female = Radiobutton(gender_frame, text="Female", variable=self.txt_gender, value=0)
        rb_male.grid(row=0, column=0, padx=(0, 12), sticky='w')
        rb_female.grid(row=0, column=1, sticky='w')

        lbl_marital_status = Label(self.student_info, text='Marital Status: ')
        lbl_marital_status.grid(row=2, column=2, padx=10, pady=6, sticky='w')
        self.int_marital_status_var = IntVar(value=0)
        marital_status_frame = Frame(self.student_info)
        marital_status_frame.grid(row=2, column=3, padx=10, pady=6, sticky='w')
        rb_single = Radiobutton(marital_status_frame, text="Single", variable=self.int_marital_status_var, value=0)
        rb_married = Radiobutton(marital_status_frame, text="Married", variable=self.int_marital_status_var, value=1)
        rb_single.grid(row=0, column=0, padx=(0, 12), sticky='w')
        rb_married.grid(row=0, column=1, sticky='w')

        lbl_mobile = Label(self.student_info, text='Mobile No.: ')
        lbl_mobile.grid(row=3, column=0, padx=10, pady=6, sticky='w')
        self.txt_mobile = StringVar()
        self.ent_mobile = Entry(self.student_info, textvariable=self.txt_mobile, width=32)
        self.ent_mobile.grid(row=3, column=1, padx=10, pady=6, sticky='w')

        lbl_email_address = Label(self.student_info, text='Email Address: ')
        lbl_email_address.grid(row=3, column=2, padx=10, pady=6, sticky='w')
        self.txt_email_address = StringVar()
        self.ent_email_address = Entry(self.student_info, textvariable=self.txt_email_address, width=32)
        self.ent_email_address.grid(row=3, column=3, padx=10, pady=6, sticky='w')

        lbl_address = Label(self.student_info, text='Address: ')
        lbl_address.grid(row=4, column=0, padx=10, pady=6, sticky='w')
        self.txt_address = StringVar()
        self.ent_address = Entry(self.student_info, textvariable=self.txt_address, width=32)
        self.ent_address.grid(row=4, column=1, padx=10, pady=6, sticky='w')

        lbl_education = Label(self.student_info, text='Education: ')
        lbl_education.grid(row=4, column=2, padx=10, pady=6, sticky='w')
        self.txt_education = StringVar()
        self.cmb_education = Combobox(self.student_info, textvariable=self.txt_education, state='readonly', width=30)
        self.cmb_education.grid(row=4, column=3, padx=10, pady=6, sticky='w')

        lbl_first_register_date = Label(self.student_info, text='First Register Date: ')
        lbl_first_register_date.grid(row=5, column=0, padx=10, pady=6, sticky='w')
        self.ent_first_register_date = DateEntry(self.student_info, width=27)
        self.ent_first_register_date.grid(row=5, column=1, padx=10, pady=6, sticky='w')

        lbl_photo = Label(self.student_info, text='Photo: ')
        lbl_photo.grid(row=6, column=0, padx=10, pady=6, sticky='nw')
        self.photo_picker = PersonPhotoPicker(self.student_info)
        self.photo_picker.grid(row=6, column=1, columnspan=3, padx=10, pady=6, sticky='w')

        lbl_student_id = Label(self.student_info, text='Student ID: ')
        lbl_student_id.grid(row=7, column=0, padx=10, pady=6, sticky='w')
        self.lbl_student_id_value = Label(self.student_info, text='')
        self.lbl_student_id_value.grid(row=7, column=1, padx=10, pady=6, sticky='w')

        lbl_search_keyword = Label(self.student_info, text='Search Keyword: ')
        lbl_search_keyword.grid(row=7, column=2, padx=10, pady=6, sticky='w')
        self.txt_search_keyword = StringVar()
        self.ent_search_keyword = Entry(self.student_info, textvariable=self.txt_search_keyword, width=32)
        self.ent_search_keyword.grid(row=7, column=3, padx=10, pady=6, sticky='w')

        search_button = Button(self.student_info, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=8, column=0, padx=10, pady=12, sticky='ew')

        register_button = Button(self.student_info, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=8, column=1, padx=10, pady=12, sticky='ew')

        update_button = Button(self.student_info, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=8, column=2, padx=10, pady=12, sticky='ew')

        delete_button = Button(self.student_info, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=8, column=3, padx=10, pady=12, sticky='ew')

        clear_button = Button(self.student_info, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=9, column=0, columnspan=4, padx=10, pady=(0, 12), sticky='ew')

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING, command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        apply_form_field_layout(self.student_info)
        apply_readonly_value_style(self.lbl_student_id_value)

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.update_existing_person_visibility()
        self.winfo_toplevel().fit_to_content(self, min_width=980, min_height=880)
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
            'lookups': self.student_bll.get_form_lookups(),
            'students': self.student_bll.search_students(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_form_lookups(data['lookups'])
        self.fill_student_tree(data['students'])

    def search(self):
        refresh_page_now(self)

    def register(self):
        try:
            self.student_bll.register_student(self.create_student_model(self.selected_existing_person_id))
            msg.showinfo('Register Student', 'Student registered successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Student Data', str(error))
        except Exception as error:
            msg.showerror('Register Student Failed', str(error))

    def update(self):
        try:
            student = self.create_student_model(self.selected_person_id)
            self.student_bll.update_student(student)
            msg.showinfo('Update Student', 'Student updated successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Student Data', str(error))
        except Exception as error:
            msg.showerror('Update Student Failed', str(error))

    def delete(self):
        try:
            if not self.selected_person_id:
                raise ValueError('Please select a student first.')

            confirm = msg.askyesno('Delete Student', 'Are you sure you want to delete this student?')
            if not confirm:
                return

            self.student_bll.delete_student(self.selected_person_id)
            msg.showinfo('Delete Student', 'Student deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('Administration', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Delete Student', str(error))
        except Exception as error:
            msg.showerror('Delete Student Failed', str(error))

    def create_student_model(self, person_id=None):
        return Student_Model_Class(
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
            first_register_date=self.get_required_date(self.ent_first_register_date, 'First Register Date'),
            **self.photo_picker.get_change()
        )

    def clear_form(self):
        self.selected_person_id = None
        self.selected_existing_person_id = None
        self.txt_existing_person.set('')
        for variable in (
                self.txt_firstname, self.txt_lastname, self.txt_national_code, self.txt_mobile,
                self.txt_email_address, self.txt_address, self.txt_education, self.txt_search_keyword):
            variable.set('')

        self.ent_birthdate.entry.delete(0, 'end')
        self.ent_first_register_date.entry.delete(0, 'end')
        self.txt_gender.set(1)
        self.int_marital_status_var.set(0)
        self.lbl_student_id_value.configure(text='')
        self.photo_picker.clear()

        for item_id in self.student_tree.selection():
            self.student_tree.selection_remove(item_id)

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
            self.txt_mobile.get().strip()
        ]

        for value in values:
            if value:
                return value

        return None

    def configure_student_tree(self):
        self.student_columns = (
            'person_id', 'full_name', 'mobile', 'register_date'
        )
        headings = {
            'person_id': 'Person ID',
            'full_name': 'Student Name',
            'mobile': 'Mobile',
            'register_date': 'Register Date'
        }

        self.student_tree.configure(columns=self.student_columns, show='headings')
        for column in self.student_columns:
            self.student_tree.heading(column, text=headings[column], anchor='w')
            self.student_tree.column(column, width=120, anchor='w', stretch=False)

        self.student_tree.column('person_id', width=140, anchor='w', stretch=False)
        self.student_tree.column('full_name', width=390, anchor='w', stretch=False)
        self.student_tree.column('mobile', width=160, anchor='w', stretch=False)
        self.student_tree.column('register_date', width=160, anchor='w', stretch=False)

    def fill_student_tree(self, students):
        self.student_rows = {}
        for item_id in self.student_tree.get_children():
            self.student_tree.delete(item_id)

        for student in students:
            item_id = self.student_tree.insert('', 'end', values=(
                student.person_id,
                f'{student.firstname} {student.lastname}'.strip(),
                student.mobile,
                student.first_register_date
            ))
            self.student_rows[item_id] = student

    def on_student_select(self, event=None):
        selected_item_ids = self.student_tree.selection()
        if not selected_item_ids:
            return

        student = self.student_rows.get(selected_item_ids[0])
        if not student:
            return

        self.selected_person_id = student.person_id
        self.selected_existing_person_id = None
        self.txt_existing_person.set('')
        self.lbl_student_id_value.configure(text=student.person_id)
        self.txt_firstname.set(student.firstname)
        self.txt_lastname.set(student.lastname)
        self.set_date_entry_text(self.ent_birthdate, student.birthdate)
        self.int_marital_status_var.set(1 if student.marital_status == 'Married' else 0)
        self.txt_national_code.set(student.national_code)
        self.txt_mobile.set(student.mobile)
        self.txt_address.set(student.address or '')
        self.txt_gender.set(1 if student.gender == 'Male' else 0)
        self.txt_email_address.set(student.email_address or '')
        self.set_lookup_value(self.txt_education, self.education_options, student.education_id)
        self.set_date_entry_text(self.ent_first_register_date, student.first_register_date)
        self.photo_picker.set_database_photo(self.student_bll.get_person_photo(student.person_id))

    def set_date_entry_text(self, date_entry, value):
        date_entry.entry.delete(0, 'end')
        if value:
            date_entry.entry.insert(0, value)

    def load_form_lookups(self):
        try:
            self.apply_form_lookups(self.student_bll.get_form_lookups())
        except Exception as error:
            msg.showerror('Student Form Setup Failed', str(error))

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
        self.lbl_student_id_value.configure(text='')
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
        self.photo_picker.set_database_photo(self.student_bll.get_person_photo(person_id))

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
