from DataAccessLayer.Teacher_CRUD_DAL import Teacher_CRUD_DAL_Class
from Model.TeacherModel import Teacher_Model_Class


class Teacher_CRUD_BLL_Class:
    def __init__(self):
        self.teacher_crud_dal_object = Teacher_CRUD_DAL_Class()

    def register_teacher(self, teacher_object: Teacher_Model_Class):
        self.validate_teacher(teacher_object)
        self.teacher_crud_dal_object.register_teacher(teacher_object)

    def search_teachers(self, keyword=None):
        return self.teacher_crud_dal_object.get_teachers(keyword)

    def update_teacher(self, teacher_object: Teacher_Model_Class):
        if not teacher_object.person_id:
            raise ValueError('Please select a teacher first.')

        self.validate_teacher(teacher_object)
        self.teacher_crud_dal_object.update_teacher(teacher_object)

    def delete_teacher(self, person_id: int):
        if not person_id:
            raise ValueError('Please select a teacher first.')

        self.teacher_crud_dal_object.delete_teacher(person_id)

    def get_form_lookups(self):
        return self.teacher_crud_dal_object.get_form_lookups()

    def get_person_photo(self, person_id):
        return self.teacher_crud_dal_object.get_person_photo(person_id)

    def validate_teacher(self, teacher_object: Teacher_Model_Class):
        if not teacher_object.firstname:
            raise ValueError('Firstname is required.')

        if not teacher_object.lastname:
            raise ValueError('Lastname is required.')

        self.validate_photo(teacher_object)

        if not teacher_object.birthdate:
            raise ValueError('Birth Date is required.')

        if not teacher_object.national_code:
            raise ValueError('National ID is required.')

        if len(teacher_object.national_code) != 10 or not teacher_object.national_code.isdigit():
            raise ValueError('National ID must be exactly 10 digits.')

        if not teacher_object.mobile:
            raise ValueError('Mobile No. is required.')

        if len(teacher_object.mobile) != 11 or not teacher_object.mobile.isdigit():
            raise ValueError('Mobile No. must be exactly 11 digits.')

        if teacher_object.gender not in ('Male', 'Female'):
            raise ValueError('Gender must be Male or Female.')

        if teacher_object.marital_status not in ('Single', 'Married'):
            raise ValueError('Marital status must be Single or Married.')

        if teacher_object.education_id is None:
            raise ValueError('Education is required.')

        if not teacher_object.insurance_number:
            raise ValueError('Insurance No. is required.')

        if len(teacher_object.insurance_number) != 7 or not teacher_object.insurance_number.isdigit():
            raise ValueError('Insurance No. must be exactly 7 digits.')

        if not teacher_object.account_number:
            raise ValueError('Account No. is required.')

        if len(teacher_object.account_number) != 16 or not teacher_object.account_number.isdigit():
            raise ValueError('Account No. must be exactly 16 digits.')

        if not teacher_object.start_date:
            raise ValueError('Start Date is required.')

    def validate_photo(self, person_object):
        photo_content = getattr(person_object, 'photo_content', None)
        if photo_content is None:
            return

        if len(photo_content) > 5 * 1024 * 1024:
            raise ValueError('Photo file must be 5 MB or smaller.')

        content_type = getattr(person_object, 'photo_content_type', None)
        if content_type not in ('image/jpeg', 'image/png'):
            raise ValueError('Photo must be a JPG or PNG image.')
