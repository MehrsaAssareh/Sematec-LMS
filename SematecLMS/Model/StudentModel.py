from datetime import date


class Student_Model_Class:
    def __init__(self,
                 student_id: int = None,
                 person_id: int = None,
                 firstname: str = None,
                 lastname: str = None,
                 birthdate: date = None,
                 marital_status: str = None,
                 national_code: str = None,
                 mobile: str = None,
                 address: str = None,
                 gender: str = None,
                  education_id: int = None,
                  email_address: str = None,
                  first_register_date: date = None,
                  has_photo: bool = False,
                  photo_content: bytes = None,
                  photo_file_name: str = None,
                 photo_content_type: str = None,
                 remove_photo: bool = False):
        self.student_id = student_id
        self.person_id = person_id
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.marital_status = marital_status
        self.national_code = national_code
        self.mobile = mobile
        self.address = address
        self.gender = gender
        self.education_id = education_id
        self.email_address = email_address
        self.first_register_date = first_register_date
        self.has_photo = has_photo
        self.photo_content = photo_content
        self.photo_file_name = photo_file_name
        self.photo_content_type = photo_content_type
        self.remove_photo = remove_photo

        self.first_name = firstname
        self.last_name = lastname
        self.birth_date = birthdate
