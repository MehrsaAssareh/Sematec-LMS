from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, DANGER, SECONDARY, Radiobutton, \
    IntVar, Combobox, SUCCESS
from tkinter import messagebox as msg, StringVar, HORIZONTAL, scrolledtext
from tkinter.ttk import Labelframe, Treeview, Scrollbar
from BusinessLogicLayer.Course_CRUD_BLL import Course_CRUD_BLL_Class
from Model.CourseModel import Course_Model_Class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh


class CourseFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.course_bll = Course_CRUD_BLL_Class()
        self.selected_course_id = None
        self.category_options = {}
        self.prerequisite_options = {}
        self.course_rows = {}
        initialize_lazy_page(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.header = Label(self, text="Course Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.course_info = Labelframe(self, text="Course Information", style=SUCCESS)
        self.course_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.course_info.grid_columnconfigure(0, weight=0)
        self.course_info.grid_columnconfigure(1, weight=1)
        self.course_info.grid_columnconfigure(2, weight=0)
        self.course_info.grid_columnconfigure(3, weight=1)

        self.course_list = Labelframe(self, text="Course List", style=SUCCESS)
        self.course_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.course_list.grid_columnconfigure(0, weight=1)
        self.course_list.grid_rowconfigure(0, weight=1)

        self.course_tree_scroll_y = Scrollbar(self.course_list)
        self.course_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.course_tree_scroll_x = Scrollbar(self.course_list, orient=HORIZONTAL)
        self.course_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.course_tree = Treeview(self.course_list, yscrollcommand=self.course_tree_scroll_y.set,
                                    xscrollcommand=self.course_tree_scroll_x.set, selectmode="extended", height=8)
        self.course_tree.grid(row=0, column=0, sticky='nsew')
        self.course_tree_scroll_y.config(command=self.course_tree.yview)
        self.course_tree_scroll_x.config(command=self.course_tree.xview)
        self.configure_course_tree()
        self.course_tree.bind('<<TreeviewSelect>>', self.on_course_select)

        lbl_course_code = Label(self.course_info, text='Course Code: ')
        lbl_course_code.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_course_code = StringVar()
        self.ent_course_code = Entry(self.course_info, textvariable=self.txt_course_code, width=32)
        self.ent_course_code.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        lbl_course_name = Label(self.course_info, text='Course Name: ')
        lbl_course_name.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.txt_course_name = StringVar()
        self.ent_course_name = Entry(self.course_info, textvariable=self.txt_course_name, width=32)
        self.ent_course_name.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        lbl_course_category = Label(self.course_info, text='Course Category: ')
        lbl_course_category.grid(row=1, column=0, padx=10, pady=6, sticky='w')
        self.txt_course_category = StringVar()
        self.cmb_course_category = Combobox(self.course_info, textvariable=self.txt_course_category,
                                            state='readonly', width=30)
        self.cmb_course_category.grid(row=1, column=1, padx=10, pady=6, sticky='w')

        lbl_prerequisite = Label(self.course_info, text='Prerequisite: ')
        lbl_prerequisite.grid(row=1, column=2, padx=10, pady=6, sticky='w')
        self.txt_prerequisite = StringVar()
        self.cmb_prerequisite = Combobox(self.course_info, textvariable=self.txt_prerequisite,
                                         state='readonly', width=30)
        self.cmb_prerequisite.grid(row=1, column=3, padx=10, pady=6, sticky='w')

        lbl_duration = Label(self.course_info, text='Duration (Hours): ')
        lbl_duration.grid(row=2, column=0, padx=10, pady=6, sticky='w')
        self.txt_duration = StringVar()
        self.ent_duration = Entry(self.course_info, textvariable=self.txt_duration, width=32)
        self.ent_duration.grid(row=2, column=1, padx=10, pady=6, sticky='w')

        lbl_cost = Label(self.course_info, text='Cost: ')
        lbl_cost.grid(row=2, column=2, padx=10, pady=6, sticky='w')
        self.txt_cost = StringVar()
        self.ent_cost = Entry(self.course_info, textvariable=self.txt_cost, width=32)
        self.ent_cost.grid(row=2, column=3, padx=10, pady=6, sticky='w')

        lbl_is_active = Label(self.course_info, text='Course Status: ')
        lbl_is_active.grid(row=3, column=0, padx=10, pady=6, sticky='w')
        self.int_is_active_var = IntVar(value=1)
        status_frame = Frame(self.course_info)
        status_frame.grid(row=3, column=1, padx=10, pady=6, sticky='w')
        rb_active = Radiobutton(status_frame, text="Active", variable=self.int_is_active_var, value=1)
        rb_active.grid(row=0, column=0, padx=(0, 12), sticky='w')
        rb_inactive = Radiobutton(status_frame, text="Inactive", variable=self.int_is_active_var, value=0)
        rb_inactive.grid(row=0, column=1, sticky='w')

        lbl_course_id = Label(self.course_info, text='Course ID: ')
        lbl_course_id.grid(row=3, column=2, padx=10, pady=6, sticky='w')
        self.lbl_course_id_value = Label(self.course_info, text='')
        self.lbl_course_id_value.grid(row=3, column=3, padx=10, pady=6, sticky='w')

        lbl_syllabus = Label(self.course_info, text='Syllabus: ')
        lbl_syllabus.grid(row=4, column=0, padx=10, pady=6, sticky='nw')
        self.txt_syllabus = scrolledtext.ScrolledText(self.course_info, width=80, height=3)
        self.txt_syllabus.grid(row=4, column=1, columnspan=3, padx=10, pady=6, sticky='ew')

        lbl_search_keyword = Label(self.course_info, text='Search Keyword: ')
        lbl_search_keyword.grid(row=5, column=0, padx=10, pady=6, sticky='w')
        self.txt_search_keyword = StringVar()
        self.ent_search_keyword = Entry(self.course_info, textvariable=self.txt_search_keyword, width=32)
        self.ent_search_keyword.grid(row=5, column=1, columnspan=3, padx=10, pady=6, sticky='ew')

        search_button = Button(self.course_info, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=6, column=0, padx=10, pady=12, sticky='ew')

        register_button = Button(self.course_info, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=6, column=1, padx=10, pady=12, sticky='ew')

        update_button = Button(self.course_info, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=6, column=2, padx=10, pady=12, sticky='ew')

        delete_button = Button(self.course_info, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=6, column=3, padx=10, pady=12, sticky='ew')

        clear_button = Button(self.course_info, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=7, column=0, columnspan=4, padx=10, pady=(0, 12), sticky='ew')

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING, command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        apply_form_field_layout(self.course_info)
        apply_readonly_value_style(self.lbl_course_id_value)

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self, min_width=1140, min_height=800)
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
            'lookups': self.course_bll.get_form_lookups(),
            'courses': self.course_bll.search_courses(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_form_lookups(data['lookups'])
        self.fill_course_tree(data['courses'])

    def search(self):
        refresh_page_now(self)

    def register(self):
        try:
            self.course_bll.register_course(self.create_course_model())
            msg.showinfo('Register Course', 'Course registered successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Course Data', str(error))
        except Exception as error:
            msg.showerror('Register Course Failed', str(error))

    def update(self):
        try:
            course = self.create_course_model(self.selected_course_id)
            self.course_bll.update_course(course)
            msg.showinfo('Update Course', 'Course updated successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Invalid Course Data', str(error))
        except Exception as error:
            msg.showerror('Update Course Failed', str(error))

    def delete(self):
        try:
            if not self.selected_course_id:
                raise ValueError('Please select a course first.')

            confirm = msg.askyesno('Delete Course', 'Are you sure you want to delete this course?')
            if not confirm:
                return

            result = self.course_bll.delete_course(self.selected_course_id)
            if result and result != 'Success':
                msg.showwarning('Delete Course', result)
                return

            msg.showinfo('Delete Course', 'Course deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
            self.main_view.mark_frames_stale('CourseTimesheet', 'CourseRegistration')
        except ValueError as error:
            msg.showwarning('Delete Course', str(error))
        except Exception as error:
            msg.showerror('Delete Course Failed', str(error))

    def create_course_model(self, course_id=None):
        return Course_Model_Class(
            course_id=course_id,
            course_code=self.get_required_int(self.txt_course_code, 'Course Code'),
            course_name=self.get_required_text(self.txt_course_name, 'Course Name'),
            duration=self.get_required_int(self.txt_duration, 'Duration'),
            syllabus=self.get_syllabus_text(),
            cost=self.get_required_int(self.txt_cost, 'Cost'),
            status=self.get_status_text(),
            course_category_id=self.get_required_lookup_id(
                self.txt_course_category,
                self.category_options,
                'Course Category'
            ),
            prerequisite_course_id=self.get_optional_lookup_id(self.txt_prerequisite, self.prerequisite_options)
        )

    def clear_form(self):
        self.selected_course_id = None
        for variable in (
                self.txt_course_code, self.txt_course_name, self.txt_course_category,
                self.txt_prerequisite, self.txt_duration, self.txt_cost, self.txt_search_keyword):
            variable.set('')

        self.txt_syllabus.delete('1.0', 'end')
        self.int_is_active_var.set(1)
        self.lbl_course_id_value.configure(text='')

        for item_id in self.course_tree.selection():
            self.course_tree.selection_remove(item_id)

    def get_required_text(self, variable, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')
        return value

    def get_required_int(self, variable, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        try:
            return int(value)
        except ValueError:
            raise ValueError(f'{field_name} must be a number.')

    def get_syllabus_text(self):
        value = self.txt_syllabus.get('1.0', 'end').strip()
        if not value:
            raise ValueError('Syllabus is required.')
        return value

    def get_status_text(self):
        return 'Active' if self.int_is_active_var.get() == 1 else 'Inactive'

    def get_optional_lookup_id(self, variable, options):
        value = variable.get().strip()
        if not value:
            return None

        return options.get(value)

    def get_required_lookup_id(self, variable, options, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        if value not in options:
            raise ValueError(f'Please choose a valid {field_name}.')

        return options[value]

    def get_search_keyword(self):
        search_keyword = self.txt_search_keyword.get().strip()
        if search_keyword:
            return search_keyword

        values = [
            self.txt_course_code.get().strip(),
            self.txt_course_name.get().strip(),
            self.txt_course_category.get().strip()
        ]

        for value in values:
            if value:
                return value

        return None

    def configure_course_tree(self):
        self.course_columns = ('id', 'code', 'name', 'category', 'duration', 'cost', 'status')
        headings = {
            'id': 'ID',
            'code': 'Code',
            'name': 'Course Name',
            'category': 'Category',
            'duration': 'Hours',
            'cost': 'Cost',
            'status': 'Status'
        }

        self.course_tree.configure(columns=self.course_columns, show='headings')
        for column in self.course_columns:
            self.course_tree.heading(column, text=headings[column], anchor='w')
            self.course_tree.column(column, width=120, anchor='w', stretch=False)

        self.course_tree.column('name', width=260, anchor='w', stretch=False)
        self.course_tree.column('category', width=200, anchor='w', stretch=False)
        self.course_tree.column('cost', width=130, anchor='w', stretch=False)

    def fill_course_tree(self, courses):
        self.course_rows = {}
        for item_id in self.course_tree.get_children():
            self.course_tree.delete(item_id)

        for course in courses:
            item_id = self.course_tree.insert('', 'end', values=(
                course.course_id,
                course.course_code,
                course.course_name,
                self.get_lookup_display_text(self.category_options, course.course_category_id),
                course.duration,
                course.cost,
                course.status
            ))
            self.course_rows[item_id] = course

    def on_course_select(self, event=None):
        selected_item_ids = self.course_tree.selection()
        if not selected_item_ids:
            return

        course = self.course_rows.get(selected_item_ids[0])
        if not course:
            return

        self.selected_course_id = course.course_id
        self.lbl_course_id_value.configure(text=course.course_id)
        self.txt_course_code.set(course.course_code)
        self.txt_course_name.set(course.course_name)
        self.set_lookup_value(self.txt_course_category, self.category_options, course.course_category_id)
        self.set_lookup_value(self.txt_prerequisite, self.prerequisite_options, course.prerequisite_course_id)
        self.txt_duration.set(course.duration)
        self.txt_cost.set(course.cost)
        self.int_is_active_var.set(1 if course.status == 'Active' else 0)
        self.txt_syllabus.delete('1.0', 'end')
        self.txt_syllabus.insert('1.0', course.syllabus or '')

    def load_form_lookups(self):
        try:
            self.apply_form_lookups(self.course_bll.get_form_lookups())
        except Exception as error:
            msg.showerror('Course Form Setup Failed', str(error))

    def apply_form_lookups(self, lookups):
        self.category_options = self.build_lookup_options(lookups['category'])
        self.prerequisite_options = self.build_lookup_options(lookups['course'], allow_empty=True)

        self.cmb_course_category.configure(values=list(self.category_options.keys()))
        self.cmb_prerequisite.configure(values=list(self.prerequisite_options.keys()))

    def build_lookup_options(self, rows, allow_empty=False):
        options = {}
        if allow_empty:
            options[''] = None

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
