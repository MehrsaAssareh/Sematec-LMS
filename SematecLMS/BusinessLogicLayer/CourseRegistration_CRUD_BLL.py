from DataAccessLayer.CourseRegistration_CRUD_DAL import CourseRegistration_CRUD_DAL_Class
from Model.CourseRegistrationModel import CourseRegistration_Model_class


class CourseRegistration_CRUD_BLL_Class:
    def __init__(self):
        self.course_registration_crud_dal_object = CourseRegistration_CRUD_DAL_Class()

    def register_course_registration(self, registration_object: CourseRegistration_Model_class):
        self.validate_course_registration(registration_object)
        self.course_registration_crud_dal_object.register_course_registration(registration_object)

    def search_course_registrations(self, keyword=None):
        return self.course_registration_crud_dal_object.get_course_registrations(keyword)

    def update_course_registration(self, registration_object: CourseRegistration_Model_class, registration_id):
        if not registration_id:
            raise ValueError('Please select a course registration first.')

        self.validate_course_registration(registration_object)
        has_certificate = self.course_registration_crud_dal_object.course_registration_has_certificate(registration_id)
        if has_certificate:
            raise ValueError('This registration already has a certificate and cannot be changed.')

        self.course_registration_crud_dal_object.update_course_registration(registration_object, registration_id)

    def delete_course_registration(self, registration_id):
        if not registration_id:
            raise ValueError('Please select a course registration first.')

        if self.course_registration_crud_dal_object.course_registration_has_certificate(registration_id):
            raise ValueError('This registration already has a certificate and cannot be deleted.')

        self.course_registration_crud_dal_object.delete_course_registration(registration_id)

    def get_form_lookups(self):
        return self.course_registration_crud_dal_object.get_form_lookups()

    def make_student_course_certificate(self, registration_id):
        if not registration_id:
            raise ValueError('Please select a course registration first.')

        return self.course_registration_crud_dal_object.make_student_course_certificate(registration_id)

    def get_student_course_certificate_pdf_data(self, registration_id):
        if not registration_id:
            raise ValueError('Please select a course registration first.')

        return self.course_registration_crud_dal_object.get_student_course_certificate_pdf_data(registration_id)

    def validate_course_registration(self, registration_object: CourseRegistration_Model_class):
        if registration_object.student_id is None:
            raise ValueError('Student is required.')

        if registration_object.course_id is None:
            raise ValueError('Course is required.')

        if registration_object.teacher_id is None:
            raise ValueError('Teacher is required.')

        if registration_object.term_number is None:
            raise ValueError('Term Number is required.')

        if registration_object.term_number <= 0:
            raise ValueError('Term Number must be greater than zero.')

        if registration_object.score is not None and (registration_object.score < 0 or registration_object.score > 100):
            raise ValueError('Final Score must be between 0 and 100.')
