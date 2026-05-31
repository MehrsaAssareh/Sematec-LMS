from DataAccessLayer.Login_CRUD_DAL import Login_CRUD_DAL
from Model.UserModel import User_Model_Class


class Login_CRUD_BLL_Class:
    def __init__(self):
        self.login_dal = Login_CRUD_DAL()

    def login_user(self, username=None, password=None):
        username = (username or '').strip()
        rows = self.login_dal.login_command(username, password)
        if not rows:
            return None

        user_row = rows[0]
        return User_Model_Class(
            user_name=user_row.UserName,
            password=None,
            firstname=user_row.FirstName,
            lastname=user_row.LastName,
            is_admin=user_row.isAdmin,
            is_active=user_row.isActive
        )
