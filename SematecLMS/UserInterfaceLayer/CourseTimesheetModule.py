from datetime import datetime
from ttkbootstrap import Frame, Label, Entry, Button, OUTLINE, WARNING, PRIMARY, INFO, SUCCESS, DANGER, SECONDARY, \
    DateEntry, Combobox
from tkinter import messagebox as msg, StringVar, HORIZONTAL, scrolledtext
from tkinter.ttk import Labelframe, Treeview, Scrollbar
from BusinessLogicLayer.CourseSchedule_CRUD_BLL import CourseSchedule_CRUD_BLL_Class
from Model.CourseScheduleModel import CourseSchedule_Model_Class
from .FormLayout import apply_form_field_layout, apply_readonly_value_style
from .PageLoad import initialize_lazy_page, mark_page_stale, refresh_page_now, schedule_page_refresh


class CourseTimesheetFrame(Frame):
    def __init__(self, main_view, window):
        super().__init__(window)

        self.main_view = main_view
        self.course_schedule_bll = CourseSchedule_CRUD_BLL_Class()
        self.selected_course_schedule_id = None
        self.course_options = {}
        self.teacher_options = {}
        self.course_schedule_rows = {}
        initialize_lazy_page(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.header = Label(self, text="Course Timesheet Page", style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.course_timesheet_info = Labelframe(self, text="Course Timesheet Information", style=SUCCESS)
        self.course_timesheet_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="ew")
        self.course_timesheet_info.grid_columnconfigure(0, weight=0)
        self.course_timesheet_info.grid_columnconfigure(1, weight=1)
        self.course_timesheet_info.grid_columnconfigure(2, weight=0)
        self.course_timesheet_info.grid_columnconfigure(3, weight=1)

        self.course_timesheet_list = Labelframe(self, text="Course Timesheet List", style=SUCCESS)
        self.course_timesheet_list.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.course_timesheet_list.grid_columnconfigure(0, weight=1)
        self.course_timesheet_list.grid_rowconfigure(0, weight=1)

        self.course_timesheet_tree_scroll_y = Scrollbar(self.course_timesheet_list)
        self.course_timesheet_tree_scroll_y.grid(row=0, column=1, rowspan=10, sticky='ns')

        self.course_timesheet_tree_scroll_x = Scrollbar(self.course_timesheet_list, orient=HORIZONTAL)
        self.course_timesheet_tree_scroll_x.grid(row=1, column=0, columnspan=10, sticky='ew')

        self.course_timesheet_tree = Treeview(self.course_timesheet_list,
                                              yscrollcommand=self.course_timesheet_tree_scroll_y.set,
                                              xscrollcommand=self.course_timesheet_tree_scroll_x.set,
                                              selectmode="extended", height=8)
        self.course_timesheet_tree.grid(row=0, column=0, sticky='nsew')
        self.course_timesheet_tree_scroll_y.config(command=self.course_timesheet_tree.yview)
        self.course_timesheet_tree_scroll_x.config(command=self.course_timesheet_tree.xview)
        self.configure_course_timesheet_tree()
        self.course_timesheet_tree.bind('<<TreeviewSelect>>', self.on_course_timesheet_select)

        lbl_course = Label(self.course_timesheet_info, text='Course: ')
        lbl_course.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_course = StringVar()
        self.cmb_course = Combobox(self.course_timesheet_info, textvariable=self.txt_course,
                                   state='readonly', width=30)
        self.cmb_course.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        lbl_teacher = Label(self.course_timesheet_info, text='Teacher: ')
        lbl_teacher.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.txt_teacher = StringVar()
        self.cmb_teacher = Combobox(self.course_timesheet_info, textvariable=self.txt_teacher,
                                    state='readonly', width=30)
        self.cmb_teacher.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        lbl_planned_beginning = Label(self.course_timesheet_info, text='Planned Start: ')
        lbl_planned_beginning.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_planned_beginning = DateEntry(self.course_timesheet_info, width=27)
        self.ent_planned_beginning.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        lbl_term_number = Label(self.course_timesheet_info, text='Term Number: ')
        lbl_term_number.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        self.txt_term_number = StringVar()
        self.ent_term_number = Entry(self.course_timesheet_info, textvariable=self.txt_term_number, width=32)
        self.ent_term_number.grid(row=1, column=3, padx=10, pady=10, sticky='w')

        lbl_duration_week = Label(self.course_timesheet_info, text='Duration (Weeks): ')
        lbl_duration_week.grid(row=2, column=0, padx=10, pady=6, sticky='w')
        self.txt_duration_week = StringVar()
        self.ent_duration_week = Entry(self.course_timesheet_info, textvariable=self.txt_duration_week, width=32)
        self.ent_duration_week.grid(row=2, column=1, padx=10, pady=6, sticky='w')

        lbl_duration_session = Label(self.course_timesheet_info, text='Hours per Session: ')
        lbl_duration_session.grid(row=2, column=2, padx=10, pady=6, sticky='w')
        self.txt_duration_session = StringVar()
        self.ent_duration_session = Entry(self.course_timesheet_info, textvariable=self.txt_duration_session, width=32)
        self.ent_duration_session.grid(row=2, column=3, padx=10, pady=6, sticky='w')

        lbl_planned_finishing = Label(self.course_timesheet_info, text='Planned Finish: ')
        lbl_planned_finishing.grid(row=3, column=0, padx=10, pady=6, sticky='w')
        self.ent_planned_finishing = DateEntry(self.course_timesheet_info, width=27)
        self.ent_planned_finishing.grid(row=3, column=1, padx=10, pady=6, sticky='w')

        lbl_actual_beginning = Label(self.course_timesheet_info, text='Actual Start: ')
        lbl_actual_beginning.grid(row=3, column=2, padx=10, pady=6, sticky='w')
        self.ent_actual_beginning = DateEntry(self.course_timesheet_info, width=27)
        self.ent_actual_beginning.grid(row=3, column=3, padx=10, pady=6, sticky='w')

        lbl_actual_duration = Label(self.course_timesheet_info, text='Actual Duration (Weeks): ')
        lbl_actual_duration.grid(row=4, column=0, padx=10, pady=6, sticky='w')
        self.txt_actual_duration = StringVar()
        self.ent_actual_duration = Entry(self.course_timesheet_info, textvariable=self.txt_actual_duration, width=32)
        self.ent_actual_duration.grid(row=4, column=1, padx=10, pady=6, sticky='w')

        lbl_actual_finishing = Label(self.course_timesheet_info, text='Actual Finish: ')
        lbl_actual_finishing.grid(row=4, column=2, padx=10, pady=6, sticky='w')
        self.ent_actual_finishing = DateEntry(self.course_timesheet_info, width=27)
        self.ent_actual_finishing.grid(row=4, column=3, padx=10, pady=6, sticky='w')

        lbl_room = Label(self.course_timesheet_info, text='Room: ')
        lbl_room.grid(row=5, column=0, padx=10, pady=6, sticky='w')
        self.txt_room = StringVar()
        self.ent_room = Entry(self.course_timesheet_info, textvariable=self.txt_room, width=32)
        self.ent_room.grid(row=5, column=1, padx=10, pady=6, sticky='w')

        lbl_capacity = Label(self.course_timesheet_info, text='Capacity: ')
        lbl_capacity.grid(row=5, column=2, padx=10, pady=6, sticky='w')
        self.txt_capacity = StringVar()
        self.ent_capacity = Entry(self.course_timesheet_info, textvariable=self.txt_capacity, width=32)
        self.ent_capacity.grid(row=5, column=3, padx=10, pady=6, sticky='w')

        lbl_schedule_id = Label(self.course_timesheet_info, text='Timesheet ID: ')
        lbl_schedule_id.grid(row=6, column=0, padx=10, pady=6, sticky='w')
        self.lbl_schedule_id_value = Label(self.course_timesheet_info, text='')
        self.lbl_schedule_id_value.grid(row=6, column=1, padx=10, pady=6, sticky='w')

        lbl_search_keyword = Label(self.course_timesheet_info, text='Search Keyword: ')
        lbl_search_keyword.grid(row=6, column=2, padx=10, pady=6, sticky='w')
        self.txt_search_keyword = StringVar()
        self.ent_search_keyword = Entry(self.course_timesheet_info, textvariable=self.txt_search_keyword, width=32)
        self.ent_search_keyword.grid(row=6, column=3, padx=10, pady=6, sticky='w')

        lbl_comments = Label(self.course_timesheet_info, text='Comments: ')
        lbl_comments.grid(row=7, column=0, padx=10, pady=6, sticky='nw')
        self.txt_comments = scrolledtext.ScrolledText(self.course_timesheet_info, width=80, height=4)
        self.txt_comments.grid(row=7, column=1, columnspan=3, padx=10, pady=6, sticky='ew')

        search_button = Button(self.course_timesheet_info, text='Search', bootstyle=OUTLINE + SUCCESS,
                               command=self.search)
        search_button.grid(row=8, column=0, padx=10, pady=(10, 4), sticky='ew')

        register_button = Button(self.course_timesheet_info, text='Register', bootstyle=SUCCESS,
                                 command=self.register)
        register_button.grid(row=8, column=1, padx=10, pady=(10, 4), sticky='ew')

        update_button = Button(self.course_timesheet_info, text='Update', bootstyle=INFO,
                               command=self.update)
        update_button.grid(row=8, column=2, padx=10, pady=(10, 4), sticky='ew')

        delete_button = Button(self.course_timesheet_info, text='Delete', bootstyle=OUTLINE + DANGER,
                               command=self.delete)
        delete_button.grid(row=8, column=3, padx=10, pady=(10, 4), sticky='ew')

        clear_button = Button(self.course_timesheet_info, text='Clear Form', bootstyle=OUTLINE + SECONDARY,
                              command=self.clear_form)
        clear_button.grid(row=9, column=0, columnspan=4, padx=10, pady=(0, 12), sticky='ew')

        self.back_button = Button(self, text='Back To Main Page', bootstyle=OUTLINE + WARNING, command=self.back)
        self.back_button.grid(row=0, column=1, pady=20, padx=10, sticky="e")

        apply_form_field_layout(self.course_timesheet_info)
        apply_readonly_value_style(self.lbl_schedule_id_value)
        self.clear_form()

    def back(self):
        self.main_view.switch('Main')

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self, min_width=1180, min_height=900)
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
            'lookups': self.course_schedule_bll.get_form_lookups(),
            'schedules': self.course_schedule_bll.search_course_schedules(request.get('keyword'))
        }

    def apply_page_data(self, data):
        self.apply_form_lookups(data['lookups'])
        self.fill_course_timesheet_tree(data['schedules'])

    def search(self):
        refresh_page_now(self)

    def register(self):
        try:
            self.course_schedule_bll.register_course_schedule(self.create_course_schedule_model())
            msg.showinfo('Register Course Timesheet', 'Course timesheet registered successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid Course Timesheet Data', str(error))
        except Exception as error:
            msg.showerror('Register Course Timesheet Failed', str(error))

    def update(self):
        try:
            schedule = self.create_course_schedule_model(self.selected_course_schedule_id)
            self.course_schedule_bll.update_course_schedule(schedule)
            msg.showinfo('Update Course Timesheet', 'Course timesheet updated successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Invalid Course Timesheet Data', str(error))
        except Exception as error:
            msg.showerror('Update Course Timesheet Failed', str(error))

    def delete(self):
        try:
            if not self.selected_course_schedule_id:
                raise ValueError('Please select a course timesheet first.')

            confirm = msg.askyesno('Delete Course Timesheet',
                                   'Are you sure you want to delete this course timesheet?')
            if not confirm:
                return

            self.course_schedule_bll.delete_course_schedule(self.selected_course_schedule_id)
            msg.showinfo('Delete Course Timesheet', 'Course timesheet deleted successfully.')
            self.clear_form()
            refresh_page_now(self)
        except ValueError as error:
            msg.showwarning('Delete Course Timesheet', str(error))
        except Exception as error:
            msg.showerror('Delete Course Timesheet Failed', str(error))

    def create_course_schedule_model(self, course_schedule_id=None):
        return CourseSchedule_Model_Class(
            course_schedule_id=course_schedule_id,
            course_id=self.get_required_lookup_id(self.txt_course, self.course_options, 'Course'),
            teacher_id=self.get_required_lookup_id(self.txt_teacher, self.teacher_options, 'Teacher'),
            term_number=self.get_required_int(self.txt_term_number, 'Term Number'),
            capacity=self.get_optional_int(self.txt_capacity, 'Capacity'),
            room_name=self.get_optional_text(self.txt_room),
            planned_beginning_date=self.get_required_date(self.ent_planned_beginning, 'Planned Start'),
            duration_week=self.get_required_int(self.txt_duration_week, 'Duration Weeks'),
            duration_session_hour=self.get_required_int(self.txt_duration_session, 'Hours per Session'),
            planned_finishing_date=self.get_required_date(self.ent_planned_finishing, 'Planned Finish'),
            actual_beginning_date=self.get_optional_date(self.ent_actual_beginning),
            actual_duration_week=self.get_optional_int(self.txt_actual_duration, 'Actual Duration Weeks'),
            actual_finishing_date=self.get_optional_date(self.ent_actual_finishing),
            comments=self.get_comments_text()
        )

    def clear_form(self):
        self.selected_course_schedule_id = None
        for variable in (
                self.txt_course, self.txt_teacher, self.txt_term_number, self.txt_duration_week,
                self.txt_duration_session, self.txt_actual_duration, self.txt_room,
                self.txt_capacity, self.txt_search_keyword):
            variable.set('')

        for date_entry in (
                self.ent_planned_beginning, self.ent_planned_finishing,
                self.ent_actual_beginning, self.ent_actual_finishing):
            date_entry.entry.delete(0, 'end')

        self.txt_comments.delete('1.0', 'end')
        self.lbl_schedule_id_value.configure(text='')

        for item_id in self.course_timesheet_tree.selection():
            self.course_timesheet_tree.selection_remove(item_id)

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

    def get_required_lookup_id(self, variable, options, field_name):
        value = variable.get().strip()
        if not value:
            raise ValueError(f'{field_name} is required.')

        if value not in options:
            raise ValueError(f'Please choose a valid {field_name}.')

        return options[value]

    def get_optional_lookup_id(self, variable, options, field_name):
        value = variable.get().strip()
        if not value:
            return None

        if value not in options:
            raise ValueError(f'Please choose a valid {field_name}.')

        return options[value]

    def get_optional_text(self, variable):
        value = variable.get().strip()
        return value if value else None

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

    def get_optional_date(self, date_entry):
        value = date_entry.entry.get().strip()
        if not value:
            return None

        for date_format in ('%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y'):
            try:
                return datetime.strptime(value, date_format).date()
            except ValueError:
                pass

        raise ValueError('Optional date fields must be valid dates when filled.')

    def get_comments_text(self):
        value = self.txt_comments.get('1.0', 'end').strip()
        return value if value else None

    def get_search_keyword(self):
        search_keyword = self.txt_search_keyword.get().strip()
        if search_keyword:
            return search_keyword

        course = self.txt_course.get().strip()
        if course:
            return course

        teacher = self.txt_teacher.get().strip()
        if teacher:
            return teacher

        room = self.txt_room.get().strip()
        if room:
            return room

        term = self.txt_term_number.get().strip()
        if term:
            return term

        return None

    def configure_course_timesheet_tree(self):
        self.course_timesheet_columns = (
            'id', 'course', 'teacher', 'term', 'room', 'planned_start', 'planned_finish',
            'duration_week', 'hours_per_session', 'status'
        )
        headings = {
            'id': 'ID',
            'course': 'Course',
            'teacher': 'Teacher',
            'term': 'Term',
            'room': 'Room',
            'planned_start': 'Planned Start',
            'planned_finish': 'Planned Finish',
            'duration_week': 'Weeks',
            'hours_per_session': 'Hours/Session',
            'status': 'Status'
        }

        self.course_timesheet_tree.configure(columns=self.course_timesheet_columns, show='headings')
        for column in self.course_timesheet_columns:
            self.course_timesheet_tree.heading(column, text=headings[column], anchor='w')
            self.course_timesheet_tree.column(column, width=100, anchor='w', stretch=False)

        self.course_timesheet_tree.column('id', width=70, anchor='w', stretch=False)
        self.course_timesheet_tree.column('course', width=220, anchor='w', stretch=False)
        self.course_timesheet_tree.column('teacher', width=180, anchor='w', stretch=False)
        self.course_timesheet_tree.column('term', width=70, anchor='w', stretch=False)
        self.course_timesheet_tree.column('room', width=90, anchor='w', stretch=False)
        self.course_timesheet_tree.column('duration_week', width=80, anchor='w', stretch=False)
        self.course_timesheet_tree.column('hours_per_session', width=100, anchor='w', stretch=False)

    def fill_course_timesheet_tree(self, schedules):
        self.course_schedule_rows = {}
        for item_id in self.course_timesheet_tree.get_children():
            self.course_timesheet_tree.delete(item_id)

        for schedule in schedules:
            item_id = self.course_timesheet_tree.insert('', 'end', values=(
                schedule.course_schedule_id,
                schedule.course_name,
                schedule.teacher_name or '',
                schedule.term_number or '',
                schedule.room_name or '',
                schedule.planned_beginning_date,
                schedule.planned_finishing_date,
                schedule.duration_week,
                schedule.duration_session_hour,
                self.get_schedule_status(schedule)
            ))
            self.course_schedule_rows[item_id] = schedule

    def on_course_timesheet_select(self, event=None):
        selected_item_ids = self.course_timesheet_tree.selection()
        if not selected_item_ids:
            return

        schedule = self.course_schedule_rows.get(selected_item_ids[0])
        if not schedule:
            return

        self.selected_course_schedule_id = schedule.course_schedule_id
        self.lbl_schedule_id_value.configure(text=schedule.course_schedule_id)
        self.set_lookup_value(self.txt_course, self.course_options, schedule.course_id)
        self.set_lookup_value(self.txt_teacher, self.teacher_options, schedule.teacher_id)
        self.txt_term_number.set(schedule.term_number or '')
        self.txt_capacity.set(schedule.capacity or '')
        self.txt_room.set(schedule.room_name or '')
        self.set_date_entry_text(self.ent_planned_beginning, schedule.planned_beginning_date)
        self.txt_duration_week.set(schedule.duration_week)
        self.txt_duration_session.set(schedule.duration_session_hour)
        self.set_date_entry_text(self.ent_planned_finishing, schedule.planned_finishing_date)
        self.set_date_entry_text(self.ent_actual_beginning, schedule.actual_beginning_date)
        self.txt_actual_duration.set(schedule.actual_duration_week or '')
        self.set_date_entry_text(self.ent_actual_finishing, schedule.actual_finishing_date)
        self.txt_comments.delete('1.0', 'end')
        self.txt_comments.insert('1.0', schedule.comments or '')

    def get_schedule_status(self, schedule):
        if schedule.actual_finishing_date:
            return 'Finished'

        if schedule.actual_beginning_date:
            return 'In Progress'

        return 'Planned'

    def set_date_entry_text(self, date_entry, value):
        date_entry.entry.delete(0, 'end')
        if value:
            date_entry.entry.insert(0, value)

    def load_form_lookups(self):
        try:
            self.apply_form_lookups(self.course_schedule_bll.get_form_lookups())
        except Exception as error:
            msg.showerror('Course Timesheet Form Setup Failed', str(error))

    def apply_form_lookups(self, lookups):
        self.course_options = self.build_lookup_options(lookups['course'])
        self.teacher_options = self.build_lookup_options(lookups['teacher'])
        self.cmb_course.configure(values=list(self.course_options.keys()))
        self.cmb_teacher.configure(values=list(self.teacher_options.keys()))

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
