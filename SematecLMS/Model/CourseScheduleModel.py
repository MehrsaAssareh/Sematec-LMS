from datetime import date


class CourseSchedule_Model_Class:
    def __init__(self,
                 course_schedule_id: int = None,
                 course_id: int = None,
                 course_name: str = None,
                 teacher_id: int = None,
                 teacher_name: str = None,
                 term_number: int = None,
                 capacity: int = None,
                 room_name: str = None,
                 planned_beginning_date: date = None,
                 duration_week: int = None,
                 duration_session_hour: int = None,
                 planned_finishing_date: date = None,
                 actual_beginning_date: date = None,
                 actual_duration_week: int = None,
                 actual_finishing_date: date = None,
                 comments: str = None):
        self.course_schedule_id = course_schedule_id
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.term_number = term_number
        self.capacity = capacity
        self.room_name = room_name
        self.planned_beginning_date = planned_beginning_date
        self.duration_week = duration_week
        self.duration_session_hour = duration_session_hour
        self.planned_finishing_date = planned_finishing_date
        self.actual_beginning_date = actual_beginning_date
        self.actual_duration_week = actual_duration_week
        self.actual_finishing_date = actual_finishing_date
        self.comments = comments
