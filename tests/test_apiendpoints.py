"""Contains tests for the api endpoints"""

import unittest

import json

from app import create_app

from app.api_1_0.models import User, Business

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
        "Name":"brunt-electronics", 
        "Description":"We sell electronics", 
        "Category":"electronics", 
        "Location":"West-Lands", 
        "Address":"1234-westy", 
        }
        self.mock_review = { "Email":"p@g.com", "Comment":"sth"}
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        # del self.user
        del self.mock_business
        del self.mock_review
        del self.user

    def test_registration(self):
        """Test that api can register a user"""
        user = {'Username':'James', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}
        response = self.client().post('/api/v1/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('James', str(response.data)) 

    def get_token(self):
        """Logs the user in to generate a token for protected routes"""
        logins = {
            "Username":"Peter",
            "Password":"pass123"
        }
        self.client().post('/api/v1/auth/register', data=self.user)
        response = self.client().post('/api/v1/auth/login', data=logins)
        token = json.loads(response.data.decode('UTF-8'))
        return token.get('token')

    def test_login(self):
        """Test api can login successfuly registered user"""
        token = self.get_token()        
        user = {'Username':'Lianca', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}
        response = self.client().post('/api/v1/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        logins = {
            "Username":"Lianca",
            "Password":"pass123"
        }
        result = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(result.status_code, 200)

    def test_token_exist(self):
        """Test api creates token successfuly"""
        token = self.get_token()
        self.assertTrue(token)

    def test_unregistered_user_login(self):
        """Test api cannot login unregistered user"""
        logins = {
            "Username":"kim",
            "Password":"pass456"
        }
        response = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(response.status_code, 403)

    def test_logout(self):
        """Test api can log user out"""
        token = self.get_token()               
        user = {'Username':'Kim', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}
        response = self.client().post('/api/v1/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.client().post('/api/v1/auth/logout', headers={'x-access-token': token})
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 401)


    def test_reset_password(self):
        """Test api can change user password"""
        token = self.get_token()        
        user = {'Username':'Ciru', 'Email':'pndungu54@gmail.com', \
        'Password':'pass123','Confirm Password':'pass123'}
        response = self.client().post('/api/v1/auth/register', data=user)
        self.assertEqual(response.status_code, 201)        
        logins = {
            "Username":"Peter",
            "Previous Password":"pass123",
            "New Password":"pass456"            
        }
        print('>>>>>>>>>>>',response.data)
        result = self.client().post('/api/v1/auth/reset-password', data=logins, headers={'x-access-token': token})
        self.assertEqual(result.status_code, 200)

    def test_create_business(self):
        """Test API can create a business successfuly (POST)"""
        token = self.get_token()
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('brunt-electronics', str(response.data))

    def test_update_business(self):
        """Test api can update a business"""
        token = self.get_token()       
        response = self.client().post('/api/v1/businesses', data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)      
        response_value = self.client().put('/api/v1/businesses/1', data = {"Location": "Nyeri"}, headers={'x-access-token': token})
        self.assertEqual(response_value.status_code, 200)
        result = self.client().get('/api/v1/businesses/1', headers={'x-access-token': token})
        self.assertIn('Nyeri', str(result.data))

    def test_delete_business(self):
        """Test whether api can delete a business"""
        token = self.get_token()       
        response = self.client().post('/api/v1/businesses', data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v1/businesses/1', headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        result = self.client().get('api/businesses/1', headers={'x-access-token': token})
        self.assertEqual(result.status_code, 404)

    def test_view_businesses(self):
        """Test that the api can retrieve all businesses"""
        token = self.get_token()               
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)
        self.assertIn('electronics', str(response.data))

    def test_get_business_by_id(self):
        """Test api can retrieve a business by id"""
        token = self.get_token()        
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        result = self.client().get('/api/v1/businesses/1', headers={'x-access-token': token})       
        self.assertEqual(result.status_code, 200)
        self.assertIn('brunt-electronics', str(result.data))

    def test_write_review(self):
        """Test api can allow user to write a review"""
        token = self.get_token()        
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business, headers={'x-access-token': token})
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v1/businesses/1/reviews', \
        data=self.mock_review)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', str(response.data))

    def retrieve_business_reviews(self):
        """Test api can retrieve all business reviews"""
        response = self.client().post('/api/v1/businesses', \
        data=self.mock_business)
        self.assertEqual(response.status_code, 201)
        review = {'Description':'Great services','owner':self.user['Username']}        
        response = self.client().post('/api/v1/businesses/1/reviews', \
        data=review)
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/api/v1/businesses/1/reviews')
        self.assertIn('Great services', str(result.data))

    
    