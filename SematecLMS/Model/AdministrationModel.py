from datetime import date


class Administration_Model_class:
    def __init__(self,
                 person_id: int = False,
                 firstname: str = None,
                 lastname: str = None,
                 birthdate: date = None,
                 marital_status: int = False,
                 national_code: str = None,
                 mobile: str = None,
                 address: str = None,
                 gender: int = False,
                 education_id: int = None,
                 email_address: str = None):
        self.person_id = person_id
        self.first_name = firstname
        self.last_name = lastname
        self.birth_date = birthdate
        self.marital_status = marital_status
        self.national_code = national_code
        self.mobile = mobile
        self.address = address
        self.gender = gender
        self.education_id = education_id
        self.email_address = email_address
