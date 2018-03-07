"""Contains tests for the api endpoints"""

import unittest

from flask import jsonify

from app import create_app

from app.api_v1.models import User, Business

class TestApi(unittest.TestCase):
    """This class tests the api endpoints
    tests:
        test_registration()
        test_encode_token()
        test_decode_token()
        test_login_unregistered_user()
        test_login()
        test_logout()
        test_reset_password()
        test_create_business()
        test_update_business()
        test_delete_business()
        test_view_businesses()
        test_write_review()
        retrieve_business_reviews()
        test_view_business_by_id()
    """
    def setUp(self):
        """Initialize the app and test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user = {'Username':'Peter', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}
        self.mock_business = {
            "Name":"James Barber",
            "Description":"We no longer sell bananas",
            "Location":"Kawangware",
            "Category":"fruit vendors"
        }
        self.mock_review = {'Description':'best mandazis ever', 'owner':self.user.['Username']}
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        del self.user
        del self.mock_business

    def test_registration(self):
        """Test that api can register a user"""
        res = self.client().post('/api/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('ptah', str(res.data)) 

    def test_login(self):
        """Test api can login successfuly registered user"""
        logins = {
            "Username":"Peter",
            "Password":"pass123"
        }
        res = self.client().post('/api/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        result = self.client().post('/api/auth/login', data=logins)
        self.assertEqual(result.status_code, 200)

    def test_encode_token(self):
        """Test api encodes token successfuly"""
        logins = {
            "Username":"Peter",
            "Password":"pass123"
        }
        res = self.client().post('/api/auth/register',
        data=self.user)
        self.assertEqual(res.status_code, 201)
        result = self.client().post('/api/auth/login', data=logins)
        self.assertIsInstance(result.data.get('token'), bytes)

    def test_decode_token(self):   
        """Test api decodes token successfully"""  
        logins = {
            "Username":"Peter",
            "Password":"pass123"
            }  
        res = self.client().post('/api/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        result = self.client().post('/api/auth/login', data=logins)
        self.assertIsInstance(result.tokens, bytes)   
   
    def test_unregistered_user_login(self):
        """Test api cannot login unregistered user"""
        logins = {
            "Username":"kim",
            "Password":"pass456"
        }
        res = self.client().post('/api/auth/login', data=logins)
        self.assertEqual(res.status_code, 403)

    def test_logout(self):
        """Test api can log user out"""
        res = self.client().post('/api/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.client().post('/api/auth/logout')
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 403)


    def test_reset_password(self):
        """Test api can change user password"""
        user = {'Username':'Jim', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}        
        logins = {
            "Username":"Jim",
            "Previous Password":"pass123",
            "New Password":"pass123"            
        }
        res = self.client().post('/api/auth/register', data=user)
        self.assertEqual(res.status_code, 201)
        response = self.client().post('/api/auth/reset-password', data=logins)
        self.assertEqual(response.status_code, 200)

    def test_create_business(self):
        """Test API can create a business successfuly (POST)"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        self.assertIn('James Barber', str(response.data))

    def test_update_business(self):
        
        pndungu54"""Test api can update a business"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        response_value = self.client().put('/api/businesses/1',
            data = {
                'Location': 'Nyeri'
            }
        )
        self.assertEqual(response_value.status_code, 200)
        result = self.client().get('/api/businesses/1')
        self.assertIn('Jebi', str(result.data))

    def test_delete_business(self):
        """Test whether api can delete a business"""
        business = {'Name':'Wakanyugi funeral services', \
        'Description':'Laying the body to rest', \
        'Category':'Funeral', 'Location':'Kirinyaga'}        
        res = self.client().post('/api/businesses', data=business)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wakanyugi funeral services', str(res.data))
        res = self.client().delete('/api/businesses/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('api/businesses/1')
        self.assertEqual(result.status_code, 404)

    def test_view_businesses(self):
        """Test that the api can retrieve all businesses"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertIn('James Barber', str(response.data))

    def test_get_business_by_id(self):
        """Test api can retrieve a business by id"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        result = self.client().get('/api/businesses/1')       
        self.assertEqual(result.status_code, 200)
        self.assertIn('James Barber', str(result.data))

    def test_write_review(self):
        """Test api can allow user to write a review"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        res = self.client().post('/api/businesses/1/reviews', \
        data=self.mock_review)
        self.assertEqual(res.status_code, 200)
        self.assertIn('mandazi', str(res.data))

    def retrieve_business_reviews(self):
        """Test api can retrieve all business reviews"""
        response = self.client().post('/api/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        review = {'Description':'Great services','owner':self.user.['Username']}        
        res = self.client().post('/api/businesses/1/reviews', \
        data=review)
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/api/businesses/1/reviews')
        self.assertIn('Great services', str(result.data))

    
    