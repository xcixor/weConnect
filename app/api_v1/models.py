"""Contains classes for modelling the app"""
import re

class User(object):
    """Defines an application user
    Attributes:

    users(list) - a list of application users
    name(str) - User's name
    email(str) - Users email address
    password(str) - Authentication password

    methods

    create_account(), login(), log_out(), reset_password(), 
    validate_email(), find_user(), 
    """
    users = []

    def __init__(self, name, email, password, confirm_password):
        self.name = name
        self.email = email
        self. password = password
        self.confirm_password = confirm_password
        
    def find_user(self):
        """Checks whether a user exists in the users list"""
        registered_user = [user for user in User.users if user['Username'] == self.name]
        if registered_user:
            return True
        return False

    def register_user(self):
        """Creates user account"""
        if self.find_user():
            return {"message":"User already exist!"}
        elif not self.verify_password_length(self.password):
            return {"message":"Password cannot be less than 6 characters!"}
        elif self.password != self.confirm_password:
            return {"message":"Passwords don't match!"}
        elif not self.verify_username(self.name):
            return {"message":"Username cannot contain special characters" } 
        elif not self.verify_email(self.email):
            return {"message":"Invalid email address!"}
        else:
            user = {'Username':self.name, 'Email':self.email, 'Password':self.password}
            User.users.append(user)
            return True

    @staticmethod
    def verify_password_length(password):
        """Check password is valid"""
        if (len(password)) >= 6:
            return True

    @staticmethod
    def verify_username(username):
        """Check password is valid"""
        if re.match("^[a-zA-Z0-9_]*$", username):
            return True

    @staticmethod
    def verify_email(email):
        """Check if email is valid"""
        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True

    @classmethod
    def get_users(cls):
        return User.users
