import os
import sys
from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, SUCCESS, DANGER, SECONDARY, \
    Combobox
from tkinter import filedialog, messagebox as msg, StringVar, HORIZONTAL
from tkinter.ttk import Labelframe, Treeview, Scrollbar
from BusinessLogicLayer.CourseRegistration_CRUD_BLL import CourseRegistration_CRUD_BLL_Class
from BusinessLogicLayer.StudentCourseCertificatePdf import (
    StudentCourseCertificatePdfGenerator,
    build_default_certificate_filename
)
from Model.CourseRegistrationModel import CourseRegistration_Model_class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh


class CourseRegistrationFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.course_registration_bll = CourseRegistration_CRUD_BLL_Class()
        self.selected_registration_key = None
        self.student_options = {}
        self.course_options = {}
        self.teacher_options = {}
        self.registration_rows = {}
        initialize_lazy_page(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.header = Label(self, text="Course Registration Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.course_registration_info = Labelframe(self, text="Course Registration Information", style=SUCCESS)
        self.course_registration_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.course_registration_info.grid_columnconfigure(0, weight=0)
        self.course_registration_info.grid_columnconfigure(1, weight=1)
        self.course_registration_info.grid_columnconfigure(2, weight=0)
        self.course_registration_info.grid_columnconfigure(3, weight=1)

        self.course_registration_list = Labelframe(self, text="Course Registration List", style=SUCCESS)
        self.course_registration_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.course_registration_list.grid_columnconfigure(0, weight=1)
        self.course_registration_list.grid_rowconfigure(0, weight=1)

        self.course_registration_tree_scroll_y = Scrollbar(self.course_registration_list)
        self.course_registration_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.course_registration_tree_scroll_x = Scrollbar(self.course_registration_list, orient=HORIZONTAL)
        self.course_registration_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.course_registration_tree = Treeview(self.course_registration_list,
                                                 yscrollcommand=self.course_registration_tree_scroll_y.set,
                                                 xscrollcommand=self.course_registration_tree_scroll_x.set,
                                                 selectmode="extended", height=10)
        self.course_registration_tree.grid(row=0, column=0, sticky='nsew')
        self.course_registration_tree_scroll_y.config(command=self.course_registration_tree.yview)
        self.course_registration_tree_scroll_x.config(command=self.course_registration_tree.xview)
        self.configure_course_registration_tree()
        self.course_registration_tree.bind('<<TreeviewSelect>>', self.on_course_registration_select)

        lbl_student = Label(self.course_registration_info, text='Student: ')
        lbl_student.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_student = StringVar()
        self.cmb_student = Combobox(self.course_registration_info, textvariable=self.txt_student,
                                    state='readonly', width=30)
        self.cmb_student.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        lbl_course = Label(self.course_registration_info, text='Course: ')
        lbl_course.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.txt_course = StringVar()
        self.cmb_course = Combobox(self.course_registration_info, textvariable=self.txt_course,
                                   state='readonly', width=30)
        self.cmb_course.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        lbl_teacher = Label(self.course_registration_info, text='Teacher: ')
        lbl_teacher.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.txt_teacher = StringVar()
        self.cmb_teacher = Combobox(self.course_registration_info, textvariable=self.txt_teacher,
                                    state='readonly', width=30)
        self.cmb_teacher.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        lbl_term_number = Label(self.course_registration_info, text='Term Number: ')
        lbl_term_number.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        self.txt_term_number = StringVar()
        self.ent_term_number = Entry(self.course_registration_info, textvariable=self.txt_term_number, width=32)
        self.ent_term_number.grid(row=1, column=3, padx=10, pady=10, sticky='w')

        lbl_final_score = Label(self.course_registration_info, text='Final Score (optional): ')
        lbl_final_score.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.txt_final_score = StringVar()
        self.ent_final_score = Entry(self.course_registration_info, textvariable=self.txt_final_score, width=32)
        self.ent_final_score.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        lbl_registration_key = Label(self.course_registration_info, text='Registration ID: ')
        lbl_registration_key.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        self.lbl_registration_key_value = Label(self.course_registration_info, text='')
        self.lbl_registration_key_value.grid(row=2, column=3, padx=10, pady=10, sticky='w')

        lbl_search_keyword = Label(self.course_registration_info, text='Search Keyword: ')
        lbl_search_keyword.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.txt_search_keyword = StringVar()
        self.ent_search_keyword = Entry(self.course_registration_info,
                                        textvariable=self.txt_search_keyword, width=32)
        self.ent_search_keyword.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        lbl_certificate_number = Label(self.course_registration_info, text='Certificate No: ')
        lbl_certificate_number.grid(row=3, column=2, padx=10, pady=10, sticky='w')
        self.lbl_certificate_number_value = Label(self.course_registration_info, text='')
        self.lbl_certificate_number_value.grid(row=3, column=3, padx=10, pady=10, sticky='w')

        lbl_certificate_issue_date = Label(self.course_registration_info, text='Certificate Date: ')
        lbl_certificate_issue_date.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.lbl_certificate_issue_date_value = Label(self.course_registration_info, text='')
        self.lbl_certificate_issue_date_value.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        certificate_button = Button(self.course_registration_info, text='Make Certificate PDF', bootstyle=PRIMARY,
                                    command=self.make_certificate)
        certificate_button.grid(row=4, column=2, padx=10, pady=12, sticky='ew')

        show_certificate_button = Button(self.course_registration_info, text='Show Certificate PDF',
                                         bootstyle=OUTLINE + INFO, command=self.show_certificate)
        show_certificate_button.grid(row=4, column=3, padx=10, pady=12, sticky='ew')

        search_button = Button(self.course_registration_info, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=5, column=0, padx=10, pady=12, sticky='ew')

        register_button = Button(self.course_registration_info, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=5, column=1, padx=10, pady=12, sticky='ew')

        update_button = Button(self.course_registration_info, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=5, column=2, padx=10, pady=12, sticky='ew')

        delete_button = Button(self.course_registration_info, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=5, column=3, padx=10, pady=12, sticky='ew')

        clear_button = Button(self.course_registration_info, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 12), sticky='ew')

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING, command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        apply_form_field_layout(self.course_registration_info)
        apply_readonly_value_style(
            self.lbl_registration_key_value,
            self.lbl_certificate_number_value,
            self.lbl_certificate_issue_date_value
        )

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self, min_width=1120, min_height=820)
        schedule_page_refresh(self)

    def mark_stale(self):
        mark_page_stale(self)

    def refresh_page(self):
        self.apply_page_data(self.load_page_data(self.get_refresh_request()))

    def get_refresh_request(self):
        return {'keyword': self.get_search_keyword()}

    def load_page_data(self, request=None):
        request = request or {}
        return {
            'lookups': self.course_registration_bll.get_form_lookups(),
            'registrations': self.course_registration_bll.search_course_registrations(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_form_lookups(data['lookups'])
        self.fill_course_registration_tree(data['registrations'])

    def search(self):
        refresh_page_now(self)

    def register(self):
        try:
            self.course_registration_bll.register_course_registration(self.create_course_registration_model())
            msg.showinfo('Register Course Registration', 'Course registration saved successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid Course Registration Data', str(error))
        except Exception as error:
            msg.showerror('Register Course Registration Failed', str(error))

    def update(self):
        try:
            registration = self.create_course_registration_model()
            self.course_registration_bll.update_course_registration(registration, self.selected_registration_key)
            msg.showinfo('Update Course Registration', 'Course registration updated successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid Course Registration Data', str(error))
        except Exception as error:
            msg.showerror('Update Course Registration Failed', str(error))

    def delete(self):
        try:
            if not self.selected_registration_key:
                raise ValueError('Please select a course registration first.')

            confirm = msg.askyesno('Delete Course Registration',
                                   'Are you sure you want to delete this course registration?')
            if not confirm:
                return

            self.course_registration_bll.delete_course_registration(self.selected_registration_key)
            msg.showinfo('Delete Course Registration', 'Course registration deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Delete Course Registration', str(error))
        except Exception as error:
            msg.showerror('Delete Course Registration Failed', str(error))

    def make_certificate(self):
        try:
            certificate = self.course_registration_bll.make_student_course_certificate(self.selected_registration_key)
            self.lbl_certificate_number_value.configure(text=certificate['certificate_number'])
            self.lbl_certificate_issue_date_value.configure(
                text=self.format_optional_date(certificate['certificate_issue_date'])
            )

            certificate_data = self.course_registration_bll.get_student_course_certificate_pdf_data(
                self.selected_registration_key
            )
            output_path = filedialog.asksaveasfilename(
                title='Where do you want to save this certificate PDF?',
                initialdir=self.get_certificate_pdf_default_folder(),
                initialfile=build_default_certificate_filename(certificate_data),
                defaultextension='.pdf',
                filetypes=(('PDF files', '*.pdf'), ('All files', '*.*'))
            )

            if not output_path:
                msg.showinfo(
                    'Make Certificate PDF',
                    f"Certificate {certificate['certificate_number']} is ready. PDF save was cancelled."
                )
                refresh_page_now(self)
                return

            saved_path = StudentCourseCertificatePdfGenerator().create_pdf(certificate_data, output_path)
            action = 'created' if certificate['created'] else 'exported'
            msg.showinfo('Make Certificate PDF', f"Certificate PDF {action} successfully:\n{saved_path}")
            self.open_certificate_pdf(saved_path)
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Make Certificate', str(error))
        except Exception as error:
            msg.showerror('Make Certificate Failed', str(error))

    def show_certificate(self):
        try:
            certificate_data = self.course_registration_bll.get_student_course_certificate_pdf_data(
                self.selected_registration_key
            )
            output_path = os.path.join(
                self.get_certificate_pdf_default_folder(),
                build_default_certificate_filename(certificate_data)
            )
            saved_path = StudentCourseCertificatePdfGenerator().create_pdf(certificate_data, output_path)
            self.open_certificate_pdf(saved_path)
        except ValueError as error:
            msg.showwarning('Show Certificate', str(error))
        except Exception as error:
            msg.showerror('Show Certificate Failed', str(error))

    def open_certificate_pdf(self, file_path):
        try:
            os.startfile(file_path)
        except OSError:
            pass

    def get_certificate_pdf_default_folder(self):
        if getattr(sys, 'frozen', False):
            app_root = os.path.dirname(sys.executable)
        else:
            app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        output_folder = os.path.join(app_root, 'GeneratedCertificates')
        os.makedirs(output_folder, exist_ok=True)
        return output_folder

    def create_course_registration_model(self):
        return CourseRegistration_Model_class(
            student_id=self.get_required_lookup_id(self.txt_student, self.student_options, 'Student'),
            course_id=self.get_required_lookup_id(self.txt_course, self.course_options, 'Course'),
            teacher_id=self.get_required_lookup_id(self.txt_teacher, self.teacher_options, 'Teacher'),
            term_number=self.get_required_int(self.txt_term_number, 'Term Number'),
            score=self.get_optional_int(self.txt_final_score, 'Final Score')
        )

    def clear_form(self):
        self.selected_registration_key = None
        for variable in (
                self.txt_student, self.txt_course, self.txt_teacher,
                self.txt_term_number, self.txt_final_score, self.txt_search_keyword):
            variable.set('')

        self.lbl_registration_key_value.configure(text='')
        self.lbl_certificate_number_value.configure(text='')
        self.lbl_certificate_issue_date_value.configure(text='')

        for item_id in self.course_registration_tree.selection():
            self.course_registration_tree.selection_remove(item_id)

    def get_required_lookup_id(self, variable, options, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        if value not in options:
            raise ValueError(f'Please choose a valid {field_name}.')

        return options[value]

    def get_required_int(self, variable, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        try:
            return int(value)
        except ValueError:
            raise ValueError(f'{field_name} must be a number.')

    def get_optional_int(self, variable, field_name):
        value = variable.get().strip()
        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            raise ValueError(f'{field_name} must be a number.')

    def get_search_keyword(self):
        search_keyword = self.txt_search_keyword.get().strip()
        if search_keyword:
            return search_keyword

        return None

    def configure_course_registration_tree(self):
        self.course_registration_columns = ('student', 'course', 'teacher', 'term', 'score', 'certificate',
                                            'issue_date')
        headings = {
            'student': 'Student',
            'course': 'Course',
            'teacher': 'Teacher',
            'term': 'Term',
            'score': 'Score',
            'certificate': 'Certificate No',
            'issue_date': 'Issue Date'
        }

        self.course_registration_tree.configure(columns=self.course_registration_columns, show='headings')
        for column in self.course_registration_columns:
            self.course_registration_tree.heading(column, text=headings[column], anchor='w')
            self.course_registration_tree.column(column, width=110, anchor='w', stretch=False)

        self.course_registration_tree.column('student', width=190, anchor='w', stretch=False)
        self.course_registration_tree.column('course', width=190, anchor='w', stretch=False)
        self.course_registration_tree.column('teacher', width=190, anchor='w', stretch=False)
        self.course_registration_tree.column('term', width=70, anchor='w', stretch=False)
        self.course_registration_tree.column('score', width=70, anchor='w', stretch=False)
        self.course_registration_tree.column('certificate', width=150, anchor='w', stretch=False)

    def fill_course_registration_tree(self, registrations):
        self.registration_rows = {}
        for item_id in self.course_registration_tree.get_children():
            self.course_registration_tree.delete(item_id)

        for registration in registrations:
            item_id = self.course_registration_tree.insert('', 'end', values=(
                registration.student_name,
                registration.course_name,
                registration.teacher_name,
                registration.term_number,
                registration.score if registration.score is not None else '',
                registration.certificate_number or '',
                self.format_optional_date(registration.certificate_issue_date)
            ))
            self.registration_rows[item_id] = registration

    def on_course_registration_select(self, event=None):
        selected_item_ids = self.course_registration_tree.selection()
        if not selected_item_ids:
            return

        registration = self.registration_rows.get(selected_item_ids[0])
        if not registration:
            return

        self.selected_registration_key = registration.registration_id
        self.lbl_registration_key_value.configure(text=registration.registration_id)
        self.set_lookup_value(self.txt_student, self.student_options, registration.student_id)
        self.set_lookup_value(self.txt_course, self.course_options, registration.course_id)
        self.set_lookup_value(self.txt_teacher, self.teacher_options, registration.teacher_id)
        self.txt_term_number.set(registration.term_number)
        self.txt_final_score.set(registration.score if registration.score is not None else '')
        self.lbl_certificate_number_value.configure(text=registration.certificate_number or '')
        self.lbl_certificate_issue_date_value.configure(
            text=self.format_optional_date(registration.certificate_issue_date)
        )

    def load_form_lookups(self):
        try:
            self.apply_form_lookups(self.course_registration_bll.get_form_lookups())
        except Exception as error:
            msg.showerror('Course Registration Form Setup Failed', str(error))

    def apply_form_lookups(self, lookups):
        self.student_options = self.build_lookup_options(lookups['student'])
        self.course_options = self.build_lookup_options(lookups['course'])
        self.teacher_options = self.build_lookup_options(lookups['teacher'])

        self.cmb_student.configure(values=list(self.student_options.keys()))
        self.cmb_course.configure(values=list(self.course_options.keys()))
        self.cmb_teacher.configure(values=list(self.teacher_options.keys()))

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

    def format_optional_date(self, value):
        return '' if value in ('', None) else str(value)
