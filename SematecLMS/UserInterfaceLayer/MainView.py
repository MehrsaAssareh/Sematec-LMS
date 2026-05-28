from tkinter import messagebox as msg

from .Window import window


class MainView:
    def __init__(self):
        self.window = window()
        self.current_user = None

        self.frames = {}
        self.frame_factories = {
            "Login": self.create_login_frame,
            "Main": self.create_main_frame,
            "Administration": self.create_administration_frame,
            "CourseRegistration": self.create_course_registration_frame,
            "CourseTimesheet": self.create_course_timesheet_frame,
            "Course": self.create_course_frame,
            "Student": self.create_student_frame,
            "Teacher": self.create_teacher_frame,
            "Employee": self.create_employee_frame
        }

        self.switch("Login")
        self.window.mainloop()

    def add_frame(self, name, frame):
        self.frames[name] = frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def get_frame(self, frame_name):
        if frame_name in self.frames:
            return self.frames[frame_name]

        if frame_name not in self.frame_factories:
            raise ValueError(f"Unknown frame: {frame_name}")

        frame = self.frame_factories[frame_name]()
        self.add_frame(frame_name, frame)
        return frame

    def switch(self, frame_name):
        if frame_name == "Administration" and not self.current_user_is_admin():
            msg.showwarning('Access Denied', 'Only admin users can open Administration.')
            return self.switch("Main") if self.current_user else self.switch("Login")

        frame = self.get_frame(frame_name)
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        return frame

    def current_user_is_admin(self):
        return bool(getattr(self.current_user, 'is_admin', False))

    def set_current_user(self, user):
        self.current_user = user

        main_frame = self.frames.get("Main")
        if main_frame and hasattr(main_frame, "set_current_user"):
            main_frame.set_current_user(user)

    def mark_frames_stale(self, *frame_names):
        for frame_name in frame_names:
            frame = self.frames.get(frame_name)
            if frame and hasattr(frame, "mark_stale"):
                frame.mark_stale()

    def create_login_frame(self):
        from .LoginModule import LoginFrame
        return LoginFrame(self, self.window)

    def create_main_frame(self):
        from .MainModule import MainFrame
        return MainFrame(self, self.window, self.current_user)

    def create_administration_frame(self):
        from .AdministrationModule import AdministrationFrame
        return AdministrationFrame(self, self.window)

    def create_course_registration_frame(self):
        from .CourseRegistrationModule import CourseRegistrationFrame
        return CourseRegistrationFrame(self, self.window)

    def create_course_timesheet_frame(self):
        from .CourseTimesheetModule import CourseTimesheetFrame
        return CourseTimesheetFrame(self, self.window)

    def create_course_frame(self):
        from .CourseModule import CourseFrame
        return CourseFrame(self, self.window)

    def create_student_frame(self):
        from .StudentModule import StudentFrame
        return StudentFrame(self, self.window)

    def create_teacher_frame(self):
        from .TeacherModule import TeacherFrame
        return TeacherFrame(self, self.window)

    def create_employee_frame(self):
        from .EmployeeModule import EmployeeFrame
        return EmployeeFrame(self, self.window)
