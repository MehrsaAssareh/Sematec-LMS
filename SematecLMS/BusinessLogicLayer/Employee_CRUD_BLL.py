from Model.EmployeeModel import Employee_Model_Class
from DataAccessLayer.Employee_CRUD_DAL import Employee_CRUD_DAL_Class


class Employee_CRUD_BLL_Class:
    def __init__(self):
        self.employee_crud_dal_object = Employee_CRUD_DAL_Class()

    def register_employee(self, employee_object: Employee_Model_Class):
        self.validate_employee(employee_object)
        self.employee_crud_dal_object.register_employee(employee_object)

    def search_employees(self, keyword=None):
        return self.employee_crud_dal_object.get_employees(keyword)

    def update_employee(self, employee_object: Employee_Model_Class):
        if not employee_object.person_id:
            raise ValueError('Please select an employee first.')

        self.validate_employee(employee_object)
        self.employee_crud_dal_object.update_employee(employee_object)

    def delete_employee(self, person_id: int):
        if not person_id:
            raise ValueError('Please select an employee first.')

        return self.employee_crud_dal_object.delete_employee(person_id)

    def get_form_lookups(self):
        return self.employee_crud_dal_object.get_form_lookups()

    def get_person_photo(self, person_id):
        return self.employee_crud_dal_object.get_person_photo(person_id)

    def validate_employee(self, employee_object: Employee_Model_Class):
        if not employee_object.firstname:
            raise ValueError('Firstname is required.')

        if not employee_object.lastname:
            raise ValueError('Lastname is required.')

        self.validate_photo(employee_object)

        if not employee_object.national_code:
            raise ValueError('National ID is required.')

        if len(employee_object.national_code) != 10 or not employee_object.national_code.isdigit():
            raise ValueError('National ID must be exactly 10 digits.')

        if not employee_object.birthdate:
            raise ValueError('Birth Date is required.')

        if not employee_object.mobile:
            raise ValueError('Mobile No. is required.')

        if len(employee_object.mobile) != 11 or not employee_object.mobile.isdigit():
            raise ValueError('Mobile No. must be exactly 11 digits.')

        if employee_object.gender not in ('Male', 'Female'):
            raise ValueError('Gender must be Male or Female.')

        if employee_object.marital_status not in ('Single', 'Married'):
            raise ValueError('Marital status must be Single or Married.')

        if employee_object.education_id is None:
            raise ValueError('Education is required.')

        if employee_object.total_children is None:
            raise ValueError('No. of Children is required.')

        if not employee_object.start_date:
            raise ValueError('Start Date is required.')

        if not employee_object.insurance_number:
            raise ValueError('Insurance No. is required.')

        if len(employee_object.insurance_number) != 7 or not employee_object.insurance_number.isdigit():
            raise ValueError('Insurance No. must be exactly 7 digits.')

        if not employee_object.account_number:
            raise ValueError('Account No. is required.')

        if len(employee_object.account_number) != 16 or not employee_object.account_number.isdigit():
            raise ValueError('Account No. must be exactly 16 digits.')

        if not employee_object.hire_date:
            raise ValueError('Hire Date is required.')

        if employee_object.department_id is None:
            raise ValueError('Department is required.')

        if employee_object.job_id is None:
            raise ValueError('Job Title is required.')

    def validate_photo(self, person_object):
        photo_content = getattr(person_object, 'photo_content', None)
        if photo_content is None:
            return

        if len(photo_content) > 5 * 1024 * 1024:
            raise ValueError('Photo file must be 5 MB or smaller.')

        content_type = getattr(person_object, 'photo_content_type', None)
        if content_type not in ('image/jpeg', 'image/png'):
            raise ValueError('Photo must be a JPG or PNG image.')
