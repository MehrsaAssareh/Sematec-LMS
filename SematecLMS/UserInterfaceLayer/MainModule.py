from ttkbootstrap import Frame, Label, Button, OUTLINE, WARNING, PRIMARY, INFO, SUCCESS
from Model.UserModel import User_Model_Class
from tkinter import messagebox as msg


class MainFrame(Frame):
    def __init__(self, main_view, window, user_param: User_Model_Class):
        super().__init__(window)

        self.main_view = main_view
        self.user = user_param

        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="main_buttons")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.header = Label(self, text='Main Page', style=PRIMARY, font=('Arial', 15, 'bold'))
        self.header.grid(row=1, column=0, columnspan=3, pady=(0, 4), padx=32)

        self.lbl_welcome = Label(self, text='', style=SUCCESS, font=('Arial', 13, 'bold'))
        self.lbl_welcome.grid(row=2, column=0, columnspan=3, pady=(0, 18), padx=32)

        self.employee_button = Button(self, text='Employee CRUD', bootstyle=OUTLINE + INFO, command=self.employee_frame)
        self.employee_button.grid(row=3, column=0, pady=10, padx=(32, 10), sticky="ew", ipady=14)

        self.teacher_button = Button(self, text='Teacher CRUD', bootstyle=OUTLINE + INFO, command=self.teacher_frame)
        self.teacher_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew", ipady=14)

        self.student_button = Button(self, text='Student CRUD', bootstyle=OUTLINE + INFO, command=self.student_frame)
        self.student_button.grid(row=3, column=2, pady=10, padx=(10, 32), sticky="ew", ipady=14)

        self.course_button = Button(self, text='Course CRUD', bootstyle=OUTLINE + INFO, command=self.course_frame)
        self.course_button.grid(row=4, column=0, pady=10, padx=(32, 10), sticky="ew", ipady=14)

        self.course_timesheet_button = Button(self, text='Course Timesheet CRUD', bootstyle=OUTLINE + INFO,
                                              command=self.course_timesheet_frame)
        self.course_timesheet_button.grid(row=4, column=1, pady=10, padx=10, sticky="ew", ipady=14)

        self.course_registration_button = Button(self, text='Course Registrations CRUD', bootstyle=OUTLINE + INFO,
                                                 command=self.course_registration_frame)
        self.course_registration_button.grid(row=4, column=2, pady=10, padx=(10, 32), sticky="ew", ipady=14)

        self.administration_button = Button(self, text='Administration CRUD', bootstyle=OUTLINE + INFO,
                                            command=self.administration_frame)
        self.administration_button.grid(row=5, column=1, pady=10, padx=10, sticky="ew", ipady=14)

        self.logout_button = Button(self, text="Logout", bootstyle=OUTLINE + WARNING, command=self.logout)
        self.logout_button.grid(row=6, column=0, columnspan=3, pady=(28, 0), padx=32, sticky="ew", ipady=8)
        self.set_current_user(user_param)

    def on_show(self):
        self.winfo_toplevel().fit_to_content(self, min_width=760, min_height=420)

    def logout(self):
        logout = msg.askyesno(title="Logout", message="Are you sure you want to logout?", icon="question")

        if logout:
            msg.showinfo("Logged out", "You have successfully logged out!\nRestarting Application...", icon="info")

            self.set_current_user(None)
            if hasattr(self.main_view, 'set_current_user'):
                self.main_view.set_current_user(None)
            self.main_view.switch('Login')

    def employee_frame(self):
        self.main_view.switch("Employee")

    def teacher_frame(self):
        self.main_view.switch("Teacher")

    def student_frame(self):
        self.main_view.switch("Student")

    def course_frame(self):
        self.main_view.switch("Course")

    def course_timesheet_frame(self):
        self.main_view.switch("CourseTimesheet")

    def course_registration_frame(self):
        self.main_view.switch("CourseRegistration")

    def administration_frame(self):
        if not self.current_user_is_admin():
            msg.showwarning('Access Denied', 'Only admin users can open Administration.')
            return

        self.main_view.switch("Administration")

    def set_current_user(self, user):
        self.user = user

        if not user:
            self.lbl_welcome.configure(text='')
            self.update_administration_access()
            return

        firstname = (user.firstname or user.user_name or '').strip()
        self.lbl_welcome.configure(text=f'Welcome {firstname}')
        self.update_administration_access()

    def current_user_is_admin(self):
        return bool(getattr(self.user, 'is_admin', False))

    def update_administration_access(self):
        if not hasattr(self, 'administration_button'):
            return

        if self.current_user_is_admin():
            self.administration_button.grid()
        else:
            self.administration_button.grid_remove()

    # if user.is_admin == 1:
    #     self.user_management_button = Button(self, text="User Management",bootstyle=OUTLINE+PRIMARY, command=self.show_user_management)
    #     self.user_management_button.grid(row=2, column=0, pady=(0, 10), padx=10, sticky="ew")

    # def show_user_management(self):
    #     user_management_frame = self.main_view.switch("user_management")
    #     user_management_frame.set_current_user(self.current_user)
