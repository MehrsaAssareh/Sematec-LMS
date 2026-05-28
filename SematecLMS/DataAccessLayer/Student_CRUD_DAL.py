import pyodbc

from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING
from DataAccessLayer.PersonLookup_DAL import PersonLookup_DAL_Class
from DataAccessLayer.PersonPhoto_DAL import PersonPhoto_DAL_Class
from Model.StudentModel import Student_Model_Class


class Student_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def __init__(self):
        self.photo_dal = PersonPhoto_DAL_Class()
        self.person_lookup_dal = PersonLookup_DAL_Class()

    def to_db_date(self, value):
        return value.isoformat() if hasattr(value, 'isoformat') else value

    def register_student(self, student_object: Student_Model_Class):
        if student_object.person_id:
            self.register_existing_person_as_student(student_object)
            return

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO dbo.Person
                    (FirstName, LastName, Birthdate, MaritalStatus, NationalCode, Mobile,
                     Address, Gender, EmailAddress, EducationID)
                OUTPUT INSERTED.ID
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_object.firstname,
                student_object.lastname,
                self.to_db_date(student_object.birthdate),
                student_object.marital_status,
                student_object.national_code,
                student_object.mobile,
                student_object.address,
                student_object.gender,
                student_object.email_address,
                student_object.education_id
            ))
            person_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO dbo.Student (PersonID, FirstRegisterDate)
                VALUES (?, ?)
            """, (
                person_id,
                self.to_db_date(student_object.first_register_date)
            ))
            self.photo_dal.apply_photo_change(cursor, person_id, student_object)
            connection.commit()

    def register_existing_person_as_student(self, student_object: Student_Model_Class):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            if self.person_lookup_dal.person_has_role(cursor, 'student', student_object.person_id):
                raise ValueError('Selected person is already a student.')

            self.person_lookup_dal.update_person(cursor, student_object)
            cursor.execute("""
                INSERT INTO dbo.Student (PersonID, FirstRegisterDate)
                VALUES (?, ?)
            """, (
                student_object.person_id,
                self.to_db_date(student_object.first_register_date)
            ))
            self.photo_dal.apply_photo_change(cursor, student_object.person_id, student_object)
            connection.commit()

    def get_students(self, keyword=None):
        command_text = """
            SELECT
                s.PersonID,
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
                CONVERT(varchar(10), s.FirstRegisterDate, 23) AS FirstRegisterDate,
                CASE WHEN pp.PersonID IS NULL THEN 0 ELSE 1 END AS HasPhoto
            FROM dbo.Student AS s
            INNER JOIN dbo.Person AS p ON p.ID = s.PersonID
            LEFT JOIN dbo.PersonPhoto AS pp ON pp.PersonID = s.PersonID
            WHERE
                ? IS NULL
                OR p.FirstName LIKE ?
                OR p.LastName LIKE ?
                OR p.NationalCode LIKE ?
                OR p.Mobile LIKE ?
            ORDER BY s.PersonID
        """
        search_value = None if not keyword else f"%{keyword}%"

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))
            rows = cursor.fetchall()

        students = []
        for row in rows:
            students.append(Student_Model_Class(
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
                first_register_date=row.FirstRegisterDate,
                has_photo=bool(row.HasPhoto)
            ))

        return students

    def update_student(self, student_object: Student_Model_Class):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE dbo.Person
                SET FirstName = ?,
                    LastName = ?,
                    Birthdate = ?,
                    MaritalStatus = ?,
                    NationalCode = ?,
                    Mobile = ?,
                    Address = ?,
                    Gender = ?,
                    EmailAddress = ?,
                    EducationID = ?
                WHERE ID = ?
            """, (
                student_object.firstname,
                student_object.lastname,
                self.to_db_date(student_object.birthdate),
                student_object.marital_status,
                student_object.national_code,
                student_object.mobile,
                student_object.address,
                student_object.gender,
                student_object.email_address,
                student_object.education_id,
                student_object.person_id
            ))

            cursor.execute("""
                UPDATE dbo.Student
                SET FirstRegisterDate = ?
                WHERE PersonID = ?
            """, (
                self.to_db_date(student_object.first_register_date),
                student_object.person_id
            ))
            self.photo_dal.apply_photo_change(cursor, student_object.person_id, student_object)
            connection.commit()

    def delete_student(self, person_id: int):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("EXEC dbo.DeleteStudent ?", person_id)
            connection.commit()

    def get_person_photo(self, person_id):
        return self.photo_dal.get_person_photo(person_id)

    def get_form_lookups(self):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, EducationTitle FROM dbo.Education ORDER BY ID")
            education_rows = cursor.fetchall()
            available_people = self.person_lookup_dal.fetch_people_available_for_role(cursor, 'student')

        return {
            'education': [(row.ID, row.EducationTitle) for row in education_rows],
            'available_people': available_people
        }
