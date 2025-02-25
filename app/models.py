from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from bson import ObjectId

class User(UserMixin):
    def __init__(self, username, email, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self._id = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self._id)

    @staticmethod
    def get_by_username(username):
        user_data = db.users.find_one({'username': username})
        if user_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash']
            )
            user._id = user_data['_id']
            return user
        return None

    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash']
            )
            user._id = user_data['_id']
            return user
        return None

    @staticmethod
    def get_by_id(user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash']
            )
            user._id = user_data['_id']
            return user
        return None


@login_manager.user_loader
def load_user(user_id):
    user = User.get_by_id(user_id)
    return user

class Contact:
    def __init__(self, mobile, email, address, reg_number, user_id):
        self.mobile = mobile
        self.email = email
        self.address = address
        self.reg_number = reg_number
        self.user_id = user_id

    def save(self):
        return db.contacts.insert_one({
            'mobile': self.mobile,
            'email': self.email,
            'address': self.address,
            'reg_number': self.reg_number,
            'user_id': self.user_id
        })

    @staticmethod
    def get_by_reg_number(reg_number):
        return db.contacts.find_one({'reg_number': reg_number})