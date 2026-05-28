from DataAccessLayer.Admin_CRUD_DAL import Admin_CRUD_DAL_Class


class Admin_CRUD_BLL_Class:
    def __init__(self):
        self.admin_dal = Admin_CRUD_DAL_Class()

    def get_people(self):
        return self.admin_dal.get_people()

    def get_person_photo(self, person_id):
        return self.admin_dal.get_person_photo(person_id)

    def search_users(self, keyword=None):
        return self.admin_dal.get_users(keyword)

    def register_user(self, user_data):
        self.validate_user(user_data)
        if self.admin_dal.username_exists(user_data['username']):
            raise ValueError('Username already exists.')

        if user_data.get('person_id') and self.admin_dal.person_link_exists(user_data['person_id']):
            raise ValueError('Selected person already has a user account.')

        self.admin_dal.register_user(user_data)

    def update_user(self, user_data):
        if not user_data.get('user_id'):
            raise ValueError('Please select a user first.')

        self.validate_user(user_data)
        if self.admin_dal.username_exists(user_data['username'], user_data['user_id']):
            raise ValueError('Username already exists.')

        if user_data.get('person_id') and self.admin_dal.person_link_exists(
                user_data['person_id'], user_data['user_id']):
            raise ValueError('Selected person already has a user account.')

        self.ensure_not_removing_last_active_admin(user_data['user_id'], user_data)
        self.admin_dal.update_user(user_data)

    def delete_user(self, user_id):
        if not user_id:
            raise ValueError('Please select a user first.')

        self.ensure_not_deleting_last_active_admin(user_id)
        self.admin_dal.delete_user(user_id)

    def ensure_not_removing_last_active_admin(self, user_id, new_user_data):
        existing_user = self.admin_dal.get_user_by_id(user_id)
        if not existing_user:
            raise ValueError('Please select a valid user first.')

        was_active_admin = bool(existing_user.isAdmin) and bool(existing_user.isActive)
        remains_active_admin = bool(new_user_data.get('is_admin')) and bool(new_user_data.get('is_active'))

        if was_active_admin and not remains_active_admin and self.admin_dal.active_admin_count() <= 1:
            raise ValueError('At least one active admin account is required.')

    def ensure_not_deleting_last_active_admin(self, user_id):
        existing_user = self.admin_dal.get_user_by_id(user_id)
        if not existing_user:
            raise ValueError('Please select a valid user first.')

        if bool(existing_user.isAdmin) and bool(existing_user.isActive) and self.admin_dal.active_admin_count() <= 1:
            raise ValueError('At least one active admin account is required.')

    def validate_user(self, user_data):
        if not user_data.get('username'):
            raise ValueError('Username is required.')

        if not user_data.get('person_id'):
            raise ValueError('Person is required.')

        is_update = bool(user_data.get('user_id'))
        password = user_data.get('password')
        confirm_password = user_data.get('confirm_password')

        if not is_update and not password:
            raise ValueError('Password is required.')

        if password or confirm_password:
            if password != confirm_password:
                raise ValueError('Password and Confirm Password must match.')

        if password and len(password) < 6:
            raise ValueError('Password must be at least 6 characters.')

        if password and len(password) > 128:
            raise ValueError('Password must be 128 characters or fewer.')

        if not password and not confirm_password and is_update:
            user_data['password'] = None
            user_data['confirm_password'] = None

        if user_data.get('confirm_password') is not None and user_data['password'] != user_data['confirm_password']:
            raise ValueError('Password and Confirm Password must match.')

        if not user_data.get('firstname'):
            raise ValueError('First name is required.')

        if not user_data.get('lastname'):
            raise ValueError('Last name is required.')

        if len(user_data['username']) > 50:
            raise ValueError('Username must be 50 characters or fewer.')
