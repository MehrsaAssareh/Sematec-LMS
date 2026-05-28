import pyodbc

from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from DataAccessLayer.PersonLookup_DAL import PersonLookup_DAL_Class
from DataAccessLayer.PersonPhoto_DAL import PersonPhoto_DAL_Class
from Model.TeacherModel import Teacher_Model_Class


class Teacher_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def __init__(self):
        self.photo_dal = PersonPhoto_DAL_Class()
        self.person_lookup_dal = PersonLookup_DAL_Class()

    def to_db_date(self, value):
        return value.isoformat() if hasattr(value, 'isoformat') else value

    def register_teacher(self, teacher_object: Teacher_Model_Class):
        if teacher_object.person_id:
            self.register_existing_person_as_teacher(teacher_object)
            return

        command_text = "EXEC [dbo].[RegisterTeacher] ?,?,?,?,?,?,?,?,?,?,?,?,?"
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                teacher_object.firstname,
                teacher_object.lastname,
                self.to_db_date(teacher_object.birthdate),
                teacher_object.marital_status,
                teacher_object.national_code,
                teacher_object.mobile,
                teacher_object.address,
                teacher_object.gender,
                teacher_object.email_address,
                teacher_object.education_id,
                teacher_object.insurance_number,
                teacher_object.account_number,
                self.to_db_date(teacher_object.start_date)
            ))
            result_row = cursor.fetchone()
            if result_row:
                self.photo_dal.apply_photo_change(cursor, result_row.PersonID, teacher_object)
            connection.commit()

    def register_existing_person_as_teacher(self, teacher_object: Teacher_Model_Class):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            if self.person_lookup_dal.person_has_role(cursor, 'teacher', teacher_object.person_id):
                raise ValueError('Selected person is already a teacher.')

            self.person_lookup_dal.update_person(cursor, teacher_object)
            cursor.execute("""
                INSERT INTO dbo.Teacher
                    (PersonID, InsuranceNumber, AccountNumber, StartDate)
                VALUES (?, ?, ?, ?)
            """, (
                teacher_object.person_id,
                teacher_object.insurance_number,
                teacher_object.account_number,
                self.to_db_date(teacher_object.start_date)
            ))
            self.photo_dal.apply_photo_change(cursor, teacher_object.person_id, teacher_object)
            connection.commit()

    def get_teachers(self, keyword=None):
        command_text = """
            SELECT
                t.PersonID,
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
                t.InsuranceNumber,
                t.AccountNumber,
                CONVERT(varchar(10), t.StartDate, 23) AS StartDate,
                CASE WHEN pp.PersonID IS NULL THEN 0 ELSE 1 END AS HasPhoto
            FROM dbo.Teacher AS t
            INNER JOIN dbo.Person AS p ON p.ID = t.PersonID
            LEFT JOIN dbo.PersonPhoto AS pp ON pp.PersonID = p.ID
            WHERE
                ? IS NULL
                OR p.FirstName LIKE ?
                OR p.LastName LIKE ?
                OR p.NationalCode LIKE ?
                OR p.Mobile LIKE ?
                OR t.InsuranceNumber LIKE ?
                OR t.AccountNumber LIKE ?
            ORDER BY t.PersonID
        """
        search_value = None if not keyword else f"%{keyword}%"

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))
            rows = cursor.fetchall()

        teachers = []
        for row in rows:
            teachers.append(Teacher_Model_Class(
                person_id=row.PersonID,
                firstname=row.FirstName,
                lastname=row.LastName,
                birthdate=row.Birthdate,
                marital_status=row.MaritalStatus,
                national_code=(row.NationalCode or '').strip(),
                mobile=(row.Mobile or '').strip(),
                address=row.Address,
                gender=row.Gender,
                education_id=row.EducationID,
                email_address=row.EmailAddress,
                insurance_number=(row.InsuranceNumber or '').strip(),
                account_number=(row.AccountNumber or '').strip(),
                start_date=row.StartDate,
                has_photo=bool(row.HasPhoto)
            ))

        return teachers

    def update_teacher(self, teacher_object: Teacher_Model_Class):
        command_text = "EXEC [dbo].[UpdateTeacher] ?,?,?,?,?,?,?,?,?,?,?,?,?,?"
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                teacher_object.person_id,
                teacher_object.firstname,
                teacher_object.lastname,
                self.to_db_date(teacher_object.birthdate),
                teacher_object.marital_status,
                teacher_object.national_code,
                teacher_object.mobile,
                teacher_object.address,
                teacher_object.gender,
                teacher_object.email_address,
                teacher_object.education_id,
                teacher_object.insurance_number,
                teacher_object.account_number,
                self.to_db_date(teacher_object.start_date)
            ))
            self.photo_dal.apply_photo_change(cursor, teacher_object.person_id, teacher_object)
            connection.commit()

    def delete_teacher(self, person_id: int):
        command_text = "EXEC [dbo].[DeleteTeacher] ?"
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, person_id)
            connection.commit()

    def get_person_photo(self, person_id):
        return self.photo_dal.get_person_photo(person_id)

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, EducationTitle FROM dbo.Education ORDER BY ID")
            education_rows = cursor.fetchall()
            available_people = self.person_lookup_dal.fetch_people_available_for_role(cursor, 'teacher')

        return {
            'education': [(row.ID, row.EducationTitle) for row in education_rows],
            'available_people': available_people
        }
