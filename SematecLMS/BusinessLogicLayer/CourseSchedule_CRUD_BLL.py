from datetime import date, datetime

from DataAccessLayer.CourseSchedule_CRUD_DAL import CourseSchedule_CRUD_DAL_Class
from Model.CourseScheduleModel import CourseSchedule_Model_Class


class CourseSchedule_CRUD_BLL_Class:
    def __init__(self):
        self.course_schedule_crud_dal_object = CourseSchedule_CRUD_DAL_Class()

    def register_course_schedule(self, schedule_object: CourseSchedule_Model_Class):
        self.validate_course_schedule(schedule_object)
        self.course_schedule_crud_dal_object.register_course_schedule(schedule_object)

    def search_course_schedules(self, keyword=None):
        return self.course_schedule_crud_dal_object.get_course_schedules(keyword)

    def update_course_schedule(self, schedule_object: CourseSchedule_Model_Class):
        if not schedule_object.course_schedule_id:
            raise ValueError('Please select a course timesheet first.')

        self.validate_course_schedule(schedule_object)
        self.course_schedule_crud_dal_object.update_course_schedule(schedule_object)

    def delete_course_schedule(self, course_schedule_id: int):
        if not course_schedule_id:
            raise ValueError('Please select a course timesheet first.')

        self.course_schedule_crud_dal_object.delete_course_schedule(course_schedule_id)

    def get_form_lookups(self):
        return self.course_schedule_crud_dal_object.get_form_lookups()

    def validate_course_schedule(self, schedule_object: CourseSchedule_Model_Class):
        if schedule_object.course_id is None:
            raise ValueError('Course is required.')

        if schedule_object.teacher_id is None:
            raise ValueError('Teacher is required.')

        if schedule_object.term_number is None:
            raise ValueError('Term Number is required.')

        if schedule_object.term_number <= 0:
            raise ValueError('Term Number must be greater than zero.')

        if schedule_object.capacity is not None and schedule_object.capacity <= 0:
            raise ValueError('Capacity must be greater than zero.')

        if schedule_object.room_name and len(schedule_object.room_name) > 50:
            raise ValueError('Room Name must be 50 characters or fewer.')

        if not schedule_object.planned_beginning_date:
            raise ValueError('Planned Start is required.')

        if schedule_object.duration_week is None:
            raise ValueError('Duration Weeks is required.')

        if schedule_object.duration_week <= 0:
            raise ValueError('Duration Weeks must be greater than zero.')

        if schedule_object.duration_session_hour is None:
            raise ValueError('Hours per Session is required.')

        if schedule_object.duration_session_hour <= 0:
            raise ValueError('Hours per Session must be greater than zero.')

        if not schedule_object.planned_finishing_date:
            raise ValueError('Planned Finish is required.')

        planned_beginning = self.to_date(schedule_object.planned_beginning_date)
        planned_finishing = self.to_date(schedule_object.planned_finishing_date)

        if planned_finishing < planned_beginning:
            raise ValueError('Planned Finish must be on or after Planned Start.')

        if schedule_object.actual_duration_week is not None and schedule_object.actual_duration_week < 0:
            raise ValueError('Actual Duration Weeks cannot be negative.')

        actual_beginning = self.to_date(schedule_object.actual_beginning_date)
        actual_finishing = self.to_date(schedule_object.actual_finishing_date)

        if actual_beginning and actual_finishing and actual_finishing < actual_beginning:
            raise ValueError('Actual Finish must be on or after Actual Start.')

        if schedule_object.comments and len(schedule_object.comments) > 500:
            raise ValueError('Comments must be 500 characters or fewer.')

    def to_date(self, value):
        if not value:
            return None

        if isinstance(value, date):
            return value

        for date_format in ('%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y'):
            try:
                return datetime.strptime(str(value), date_format).date()
            except ValueError:
                pass

        raise ValueError('Date value must be a valid date.')
