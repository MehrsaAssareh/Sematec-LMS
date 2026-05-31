from DataAccessLayer.Course_CRUD_DAL import Course_CRUD_DAL_Class
from Model.CourseModel import Course_Model_Class


class Course_CRUD_BLL_Class:
    def __init__(self):
        self.course_crud_dal_object = Course_CRUD_DAL_Class()

    def register_course(self, course_object: Course_Model_Class):
        self.validate_course(course_object)
        self.course_crud_dal_object.register_course(course_object)

    def search_courses(self, keyword=None):
        return self.course_crud_dal_object.get_courses(keyword)

    def update_course(self, course_object: Course_Model_Class):
        if not course_object.course_id:
            raise ValueError('Please select a course first.')

        self.validate_course(course_object)
        self.course_crud_dal_object.update_course(course_object)

    def delete_course(self, course_id: int):
        if not course_id:
            raise ValueError('Please select a course first.')

        return self.course_crud_dal_object.delete_course(course_id)

    def get_form_lookups(self):
        return self.course_crud_dal_object.get_form_lookups()

    def validate_course(self, course_object: Course_Model_Class):
        if course_object.course_code is None:
            raise ValueError('Course Code is required.')

        if not course_object.course_name:
            raise ValueError('Course Name is required.')

        if course_object.duration is None:
            raise ValueError('Duration is required.')

        if course_object.duration <= 0:
            raise ValueError('Duration must be greater than zero.')

        if not course_object.syllabus:
            raise ValueError('Syllabus is required.')

        if course_object.cost is None:
            raise ValueError('Cost is required.')

        if course_object.cost < 0:
            raise ValueError('Cost cannot be negative.')

        if course_object.course_category_id is None:
            raise ValueError('Course Category is required.')

        if course_object.course_id and course_object.prerequisite_course_id == course_object.course_id:
            raise ValueError('A course cannot be its own prerequisite.')

        if not course_object.status:
            raise ValueError('Course Status is required.')

        if len(course_object.course_name) > 50:
            raise ValueError('Course Name must be 50 characters or fewer.')
