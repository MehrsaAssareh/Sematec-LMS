from Model.EmployeeModel import Employee_Model_Class
import pyodbc
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from DataAccessLayer.PersonLookup_DAL import PersonLookup_DAL_Class
from DataAccessLayer.PersonPhoto_DAL import PersonPhoto_DAL_Class


class Employee_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def __init__(self):
        self.photo_dal = PersonPhoto_DAL_Class()
        self.person_lookup_dal = PersonLookup_DAL_Class()

    def to_db_date(self, value):
        return value.isoformat() if hasattr(value, 'isoformat') else value

    def register_employee(self, employee_object: Employee_Model_Class):
        if employee_object.person_id:
            self.register_existing_person_as_employee(employee_object)
            return

        command_text: str = """
            EXEC dbo.RegisterEmployee
                @FirstName = ?,
                @LastName = ?,
                @Birthdate = ?,
                @MaritalStatus = ?,
                @NationalCode = ?,
                @Mobile = ?,
                @Address = ?,
                @Gender = ?,
                @EmailAddress = ?,
                @EducationID = ?,
                @TotalChildren = ?,
                @StartDate = ?,
                @InsuranceNumber = ?,
                @AccountNumber = ?,
                @HireDate = ?,
                @DepartmentID = ?,
                @JobID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (employee_object.firstname, employee_object.lastname,
                                          self.to_db_date(employee_object.birthdate), employee_object.marital_status,
                                          employee_object.national_code, employee_object.mobile,
                                          employee_object.address,
                                          employee_object.gender, employee_object.email_address,
                                          employee_object.education_id,
                                          employee_object.total_children, self.to_db_date(employee_object.start_date),
                                          employee_object.insurance_number, employee_object.account_number,
                                          self.to_db_date(employee_object.hire_date), employee_object.department_id,
                                          employee_object.job_id))
            result_row = cursor.fetchone()
            if result_row:
                self.photo_dal.apply_photo_change(cursor, result_row.PersonID, employee_object)
            connection.commit()

    def register_existing_person_as_employee(self, employee_object: Employee_Model_Class):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            if self.person_lookup_dal.person_has_role(cursor, 'employee', employee_object.person_id):
                raise ValueError('Selected person is already an employee.')

            self.person_lookup_dal.update_person(cursor, employee_object)
            cursor.execute("""
                INSERT INTO dbo.Employee
                    (PersonID, TotalChildren, StartDate, InsuranceNumber,
                     AccountNumber, HireDate, DepartmentID, JobID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                employee_object.person_id,
                employee_object.total_children,
                self.to_db_date(employee_object.start_date),
                employee_object.insurance_number,
                employee_object.account_number,
                self.to_db_date(employee_object.hire_date),
                employee_object.department_id,
                employee_object.job_id
            ))
            self.photo_dal.apply_photo_change(cursor, employee_object.person_id, employee_object)
            connection.commit()

    def get_employees(self, keyword=None):
        command_text = """
            SELECT
                e.PersonID,
                p.FirstName,
                p.LastName,
                CONVERT(varchar(10), p.Birthdate, 23) AS Birthdate,
                p.MaritalStatus,
                p.NationalCode,
                p.Mobile,
                p.Address,
                p.Gender,
                p.EmailAddress,
                p.EducationID,
                e.TotalChildren,
                CONVERT(varchar(10), e.StartDate, 23) AS StartDate,
                e.InsuranceNumber,
                e.AccountNumber,
                CONVERT(varchar(10), e.HireDate, 23) AS HireDate,
                e.DepartmentID,
                e.JobID,
                CASE WHEN pp.PersonID IS NULL THEN 0 ELSE 1 END AS HasPhoto
            FROM dbo.Employee AS e
            INNER JOIN dbo.Person AS p ON p.ID = e.PersonID
            LEFT JOIN dbo.PersonPhoto AS pp ON pp.PersonID = p.ID
            WHERE
                ? IS NULL
                OR p.FirstName LIKE ?
                OR p.LastName LIKE ?
                OR p.NationalCode LIKE ?
                OR p.Mobile LIKE ?
            ORDER BY e.PersonID
        """
        search_value = None if not keyword else f"%{keyword}%"

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (search_value, search_value, search_value, search_value, search_value))
            rows = cursor.fetchall()

        employees = []
        for row in rows:
            employees.append(Employee_Model_Class(
                person_id=row.PersonID,
                firstname=row.FirstName,
                lastname=row.LastName,
                birthdate=row.Birthdate,
                marital_status=row.MaritalStatus,
                national_code=row.NationalCode,
                mobile=row.Mobile,
                address=row.Address,
                gender=row.Gender,
                education_id=row.EducationID,
                email_address=row.EmailAddress,
                total_children=row.TotalChildren,
                start_date=row.StartDate,
                insurance_number=row.InsuranceNumber,
                account_number=row.AccountNumber,
                hire_date=row.HireDate,
                department_id=row.DepartmentID,
                job_id=row.JobID,
                has_photo=bool(row.HasPhoto)
            ))

        return employees

    def update_employee(self, employee_object: Employee_Model_Class):
        command_text = """
            EXEC dbo.UpdateEmployee
                @PersonID = ?,
                @FirstName = ?,
                @LastName = ?,
                @Birthdate = ?,
                @MaritalStatus = ?,
                @NationalCode = ?,
                @Mobile = ?,
                @Address = ?,
                @Gender = ?,
                @EmailAddress = ?,
                @EducationID = ?,
                @TotalChildren = ?,
                @StartDate = ?,
                @InsuranceNumber = ?,
                @AccountNumber = ?,
                @HireDate = ?,
                @DepartmentID = ?,
                @JobID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text,
                           (employee_object.person_id, employee_object.firstname, employee_object.lastname,
                            self.to_db_date(employee_object.birthdate), employee_object.marital_status,
                            employee_object.national_code, employee_object.mobile, employee_object.address,
                            employee_object.gender, employee_object.email_address, employee_object.education_id,
                            employee_object.total_children, self.to_db_date(employee_object.start_date),
                            employee_object.insurance_number, employee_object.account_number,
                            self.to_db_date(employee_object.hire_date), employee_object.department_id,
                            employee_object.job_id))
            self.photo_dal.apply_photo_change(cursor, employee_object.person_id, employee_object)
            connection.commit()

    def get_person_photo(self, person_id):
        return self.photo_dal.get_person_photo(person_id)

    def delete_employee(self, person_id: int):
        command_text = "EXEC [dbo].[DeleteEmployee] ?"
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, person_id)
            result_row = cursor.fetchone()
            connection.commit()

        if result_row:
            return result_row[0]

        return None

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT ID, EducationTitle FROM dbo.Education ORDER BY ID")
            education_rows = cursor.fetchall()

            cursor.execute("SELECT ID, DepartmentName FROM dbo.Department ORDER BY ID")
            department_rows = cursor.fetchall()

            cursor.execute("SELECT ID, JobTitle FROM dbo.Job ORDER BY ID")
            job_rows = cursor.fetchall()

            available_people = self.person_lookup_dal.fetch_people_available_for_role(cursor, 'employee')

        return {
            'education': [(row.ID, row.EducationTitle) for row in education_rows],
            'department': [(row.ID, row.DepartmentName) for row in department_rows],
            'job': [(row.ID, row.JobTitle) for row in job_rows],
            'available_people': available_people
        }


Employee_CRUD_DAL_CLass = Employee_CRUD_DAL_Class
