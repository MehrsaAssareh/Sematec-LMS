from datetime import date


class Employee_Model_Class:
    def __init__(self,
                 employee_id: int = False,
                 person_id: int = False,
                 firstname: str = None,
                 lastname: str = None,
                 birthdate: date = None,
                 marital_status: str = None,
                 national_code: str = None,
                 mobile: str = None,
                 address: str = None,
                 gender: str = None,
                 education_id: int = False,
                 email_address: str = None,
                 job_id: int = False,
                 department_id: int = False,
                 total_children: int = False,
                 hire_date: date = None,
                 insurance_number: str = None,
                 account_number: str = None,
                 start_date: date = None,
                 has_photo: bool = False,
                 photo_content: bytes = None,
                 photo_file_name: str = None,
                 photo_content_type: str = None,
                 remove_photo: bool = False):
        self.employee_id = employee_id
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
        self.job_id = job_id
        self.department_id = department_id
        self.total_children = total_children
        self.hire_date = hire_date
        self.insurance_number = insurance_number
        self.account_number = account_number
        self.start_date = start_date
        self.has_photo = has_photo
        self.photo_content = photo_content
        self.photo_file_name = photo_file_name
        self.photo_content_type = photo_content_type
        self.remove_photo = remove_photo
