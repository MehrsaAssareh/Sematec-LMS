class User_Model_Class:
    def __init__(self,
                 user_name: None,
                 password: None,
                 firstname: str = None,
                 lastname: str = None,
                 is_admin: int = False,
                 is_active: int = False):
        self.user_name = user_name
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.is_admin = is_admin
        self.is_active = is_active
