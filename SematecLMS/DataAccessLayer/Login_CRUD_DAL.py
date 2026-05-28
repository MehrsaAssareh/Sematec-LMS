import pyodbc
from DataAccessLayer.AuthSecurity import verify_password
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING


class Login_CRUD_DAL:
    def login_command(self, username=None, password=None):
        command_text = """
            SELECT
                ID,
                UserName,
                FirstName,
                LastName,
                isAdmin,
                isActive,
                PasswordHash,
                PasswordSalt,
                PasswordIterations
            FROM dbo.Users
            WHERE UserName = ?
              AND isActive = 1
        """

        with pyodbc.connect(DB_CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute(command_text, username)
            rows = cursor.fetchall()
            if not rows:
                return []

            user = rows[0]
            if verify_password(password, user.PasswordSalt, user.PasswordHash, user.PasswordIterations):
                return [user]

            return []
