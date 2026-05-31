import pyodbc
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING


class PersonLookup_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING
    ROLE_TABLES = {
        'employee': 'Employee',
        'teacher': 'Teacher',
        'student': 'Student'
    }

    def get_people_available_for_role(self, role_name):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            return self.fetch_people_available_for_role(cursor, role_name)

    def fetch_people_available_for_role(self, cursor, role_name):
        role_table = self.get_role_table(role_name)
        command_text = f"""
            SELECT
                p.ID,
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
                CASE WHEN pp.PersonID IS NULL THEN 0 ELSE 1 END AS HasPhoto
            FROM dbo.Person AS p
            LEFT JOIN dbo.{role_table} AS role_table ON role_table.PersonID = p.ID
            LEFT JOIN dbo.PersonPhoto AS pp ON pp.PersonID = p.ID
            WHERE role_table.PersonID IS NULL
            ORDER BY p.LastName, p.FirstName, p.ID
        """
        cursor.execute(command_text)
        return [self.row_to_person(row) for row in cursor.fetchall()]

    def person_has_role(self, cursor, role_name, person_id):
        role_table = self.get_role_table(role_name)
        cursor.execute(f"SELECT COUNT(1) FROM dbo.{role_table} WHERE PersonID = ?", person_id)
        return cursor.fetchone()[0] > 0

    def update_person(self, cursor, person_object):
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
            person_object.firstname,
            person_object.lastname,
            self.to_db_date(person_object.birthdate),
            person_object.marital_status,
            person_object.national_code,
            person_object.mobile,
            person_object.address,
            person_object.gender,
            person_object.email_address,
            person_object.education_id,
            person_object.person_id
        ))

    def get_role_table(self, role_name):
        role_table = self.ROLE_TABLES.get(role_name.lower())
        if not role_table:
            raise ValueError(f"Unknown person role: {role_name}")
        return role_table

    def row_to_person(self, row):
        return {
            'person_id': row.ID,
            'firstname': row.FirstName,
            'lastname': row.LastName,
            'birthdate': row.Birthdate,
            'marital_status': row.MaritalStatus,
            'national_code': (row.NationalCode or '').strip(),
            'mobile': (row.Mobile or '').strip(),
            'address': row.Address,
            'gender': row.Gender,
            'email_address': row.EmailAddress,
            'education_id': row.EducationID,
            'has_photo': bool(row.HasPhoto)
        }

    def to_db_date(self, value):
        return value.isoformat() if hasattr(value, 'isoformat') else value
