from DataAccessLayer.Student_CRUD_DAL import Student_CRUD_DAL_Class
from Model.StudentModel import Student_Model_Class


class Student_CRUD_BLL_Class:
    def __init__(self):
        self.student_crud_dal_object = Student_CRUD_DAL_Class()

    def register_student(self, student_object: Student_Model_Class):
        self.validate_student(student_object)
        self.student_crud_dal_object.register_student(student_object)

    def search_students(self, keyword=None):
        return self.student_crud_dal_object.get_students(keyword)

    def update_student(self, student_object: Student_Model_Class):
        if not student_object.person_id:
            raise ValueError('Please select a student first.')

        self.validate_student(student_object)
        self.student_crud_dal_object.update_student(student_object)

    def delete_student(self, person_id: int):
        if not person_id:
            raise ValueError('Please select a student first.')

        self.student_crud_dal_object.delete_student(person_id)

    def get_form_lookups(self):
        return self.student_crud_dal_object.get_form_lookups()

    def get_person_photo(self, person_id):
        return self.student_crud_dal_object.get_person_photo(person_id)

    def validate_student(self, student_object: Student_Model_Class):
        if not student_object.firstname:
            raise ValueError('Firstname is required.')

        if not student_object.lastname:
            raise ValueError('Lastname is required.')

        self.validate_photo(student_object)

        if not student_object.birthdate:
            raise ValueError('Birth Date is required.')

        if not student_object.national_code:
            raise ValueError('National ID is required.')

        if len(student_object.national_code) != 10 or not student_object.national_code.isdigit():
            raise ValueError('National ID must be exactly 10 digits.')

        if not student_object.mobile:
            raise ValueError('Mobile No. is required.')

        if len(student_object.mobile) != 11 or not student_object.mobile.isdigit():
            raise ValueError('Mobile No. must be exactly 11 digits.')

        if student_object.gender not in ('Male', 'Female'):
            raise ValueError('Gender must be Male or Female.')

        if student_object.marital_status not in ('Single', 'Married'):
            raise ValueError('Marital status must be Single or Married.')

        if student_object.education_id is None:
            raise ValueError('Education is required.')

        if not student_object.first_register_date:
            raise ValueError('First Register Date is required.')

    def validate_photo(self, person_object):
        photo_content = getattr(person_object, 'photo_content', None)
        if photo_content is None:
            return

        if len(photo_content) > 5 * 1024 * 1024:
            raise ValueError('Photo file must be 5 MB or smaller.')

        content_type = getattr(person_object, 'photo_content_type', None)
        if content_type not in ('image/jpeg', 'image/png'):
            raise ValueError('Photo must be a JPG or PNG image.')
