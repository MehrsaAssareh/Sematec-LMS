import pyodbc
from DataAccessLayer.AuthSecurity import hash_password
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING


class Admin_CRUD_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def get_people(self):
        command_text = """
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
                ed.EducationTitle,
                CASE WHEN pp.PersonID IS NULL THEN 0 ELSE 1 END AS HasPhoto,
                CASE WHEN u.PersonID IS NULL THEN 0 ELSE 1 END AS HasUser,
                LTRIM(RTRIM(CONCAT(
                    CASE WHEN emp.PersonID IS NOT NULL THEN 'Employee ' ELSE '' END,
                    CASE WHEN teacher.PersonID IS NOT NULL THEN 'Teacher ' ELSE '' END,
                    CASE WHEN student.PersonID IS NOT NULL THEN 'Student' ELSE '' END
                ))) AS Roles
            FROM dbo.Person p
            LEFT JOIN dbo.Education ed ON ed.ID = p.EducationID
            LEFT JOIN (SELECT DISTINCT PersonID FROM dbo.Employee) emp ON emp.PersonID = p.ID
            LEFT JOIN (SELECT DISTINCT PersonID FROM dbo.Teacher) teacher ON teacher.PersonID = p.ID
            LEFT JOIN (SELECT DISTINCT PersonID FROM dbo.Student) student ON student.PersonID = p.ID
            LEFT JOIN dbo.PersonPhoto pp ON pp.PersonID = p.ID
            LEFT JOIN dbo.Users u ON u.PersonID = p.ID
            ORDER BY p.LastName, p.FirstName
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text)
            return cursor.fetchall()

    def get_users(self, keyword=None):
        command_text = """
            SELECT
                u.ID,
                u.UserName,
                CAST(NULL AS varchar(50)) AS Password,
                u.FirstName,
                u.LastName,
                u.isAdmin,
                u.isActive,
                u.PersonID,
                p.FirstName + N' ' + p.LastName AS PersonName
            FROM dbo.Users u
            INNER JOIN dbo.Person p ON p.ID = u.PersonID
            WHERE
                ? IS NULL
                OR u.UserName LIKE ?
                OR u.FirstName LIKE ?
                OR u.LastName LIKE ?
                OR p.FirstName LIKE ?
                OR p.LastName LIKE ?
            ORDER BY u.ID
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
                search_value
            ))
            return cursor.fetchall()

    def username_exists(self, username, user_id=None):
        command_text = """
            SELECT COUNT(1)
            FROM dbo.Users
            WHERE UserName = ? AND (? IS NULL OR ID <> ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (username, user_id, user_id))
            return cursor.fetchone()[0] > 0

    def person_link_exists(self, person_id, user_id=None):
        command_text = """
            SELECT COUNT(1)
            FROM dbo.Users
            WHERE PersonID = ? AND (? IS NULL OR ID <> ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (person_id, user_id, user_id))
            return cursor.fetchone()[0] > 0

    def get_user_by_id(self, user_id):
        command_text = """
            SELECT
                ID,
                UserName,
                FirstName,
                LastName,
                isAdmin,
                isActive,
                PersonID
            FROM dbo.Users
            WHERE ID = ?
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, user_id)
            return cursor.fetchone()

    def active_admin_count(self):
        command_text = """
            SELECT COUNT(1)
            FROM dbo.Users
            WHERE isAdmin = 1
              AND isActive = 1
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text)
            return cursor.fetchone()[0]

    def register_user(self, user_data):
        salt, password_hash, iterations = hash_password(user_data['password'])
        command_text = """
            INSERT INTO dbo.Users
                (UserName, PasswordHash, PasswordSalt, PasswordIterations,
                 FirstName, LastName, isAdmin, isActive, PersonID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, (
                user_data['username'],
                password_hash,
                salt,
                iterations,
                user_data['firstname'],
                user_data['lastname'],
                user_data['is_admin'],
                user_data['is_active'],
                user_data.get('person_id')
            ))
            connection.commit()

    def update_user(self, user_data):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            if user_data.get('password'):
                salt, password_hash, iterations = hash_password(user_data['password'])
                cursor.execute("""
                    UPDATE dbo.Users
                    SET UserName = ?,
                        PasswordHash = ?,
                        PasswordSalt = ?,
                        PasswordIterations = ?,
                        FirstName = ?,
                        LastName = ?,
                        isAdmin = ?,
                        isActive = ?,
                        PersonID = ?
                    WHERE ID = ?
                """, (
                    user_data['username'],
                    password_hash,
                    salt,
                    iterations,
                    user_data['firstname'],
                    user_data['lastname'],
                    user_data['is_admin'],
                    user_data['is_active'],
                    user_data.get('person_id'),
                    user_data['user_id']
                ))
            else:
                cursor.execute("""
                    UPDATE dbo.Users
                    SET UserName = ?,
                        FirstName = ?,
                        LastName = ?,
                        isAdmin = ?,
                        isActive = ?,
                        PersonID = ?
                    WHERE ID = ?
                """, (
                    user_data['username'],
                    user_data['firstname'],
                    user_data['lastname'],
                    user_data['is_admin'],
                    user_data['is_active'],
                    user_data.get('person_id'),
                    user_data['user_id']
                ))
            connection.commit()

    def delete_user(self, user_id):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM dbo.Users WHERE ID = ?", user_id)
            connection.commit()

    def get_person_photo(self, person_id):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT PhotoContent, FileName, ContentType
                FROM dbo.PersonPhoto
                WHERE PersonID = ?
            """, person_id)
            row = cursor.fetchone()

        if not row:
            return None

        return {
            'content': bytes(row.PhotoContent),
            'file_name': row.FileName,
            'content_type': row.ContentType
        }
