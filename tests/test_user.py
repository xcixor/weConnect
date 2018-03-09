"""Contains tests for User class"""

import unittest

from app.api_1_0.models import User

class TestUserCase(unittest.TestCase):
    """
    Tests User class functionality
    tests:
        test_register_user()
        test_cannot_create_duplicate_user()
        test_valid_username()
        test_valid_email()
        test_valid_password_length()
        test_passwords_match()
        test_login()
        test_logout()
        test_reset_password()
        test_reset_password_with_wrong_previous_password()
    """
    def setUp(self):
        self.success_user = User('ptah', 'pndungu54@gmail.com',\
        'pass123', 'pass123')

    def tearDown(self):
        del self.success_user

    def test_register_user(self):
        """Test app can create a user successfully"""
        self.success_user.register_user()
        response = User.get_users()
        self.assertEqual(response, \
        [{'Username':'ptah', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123'}])

    def test_duplicate_users(self):
        """Test app cannot create duplicate users"""
        self.success_user.register_user()
        response = self.success_user.register_user()
        self.assertEqual(response['message'], 'User already exist!')

    def test_valid_username(self):
        """Test app does not allow invalid username,
        i.e containing special characters"""
        user = User('2@#$#', 'user@yahoo.com', 'pass123', 'pass123')
        response = user.register_user()
        self.assertEqual(response['message'], 
        'Username cannot contain special characters')

    def test_valid_email(self):
        """Test app cannot allow invalid email"""
        user = User('ciru', 'shi.xyx', 'pass123', 'pass123')
        response = user.register_user()
        self.assertEqual(response['message'], 'Invalid email address!')

    def test_passwords_match(self):
        """Test passwords match before user"""
        user = User('keshi', 'keshi@gmail.com', 'pass123', 'pass456')
        response = user.register_user()
        self.assertTrue(response['message'], 'Passwords dont match!')

    def test_valid_password_length(self):
        """Test password is greater or equal to six characters!"""
        user = User('Jini', 'jin@g.com','jin1', 'jin1')
        response = user.register_user()
        self.assertTrue(response['message'], 
        'Password cannot be less than 6 characters!')

    def test_login(self):
        """Test user can logout successfuly"""
        self.success_user.register_user()
        response  = self.success_user.login('ptah', 'pass123')
        self.assertTrue(response)

    def test_logout(self):
        """Test user can logout successfully"""
        self.success_user.register_user()
        self.success_user.login('ptah', 'pass123')
        response = self.success_user.log_out()
        self.assertTrue(response)

    def test_reset_password(self):
        """Test app can allow reset password"""
        self.success_user.register_user()
        result = User.reset_password(self.success_user.name,'pass123', 
        '123pass')
        self.assertEqual(result['message'], 'Password successfully changed')

    def test_reset_password_with_wrong_previous_password(self):
        self.success_user.register_user()
        result = User.reset_password(self.success_user.name, 'wrong345', 
        'new1234')
        self.assertEqual(result['message'], 'Previous password incorrect')
