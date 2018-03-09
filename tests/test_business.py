"""Contains test for the Business class"""

import unittest

from app.api_1_0.models import Business, User

class TestBusinessCase(unittest.TestCase):
    """Test Business class functionality
    Attributes:
        business(obj): a business object to be used for \
        subsequent tests
    Methods:
        test_create_business()
        test_cannot_create_duplicate_businesses()
        test_create_business()
        test_edit_business()
        test_delete_business()
        test_find_business_by_id()
        test_find_businesses_by_category()
        test_find_businesses_by_location()
        test_write_review()
        test_get_all_reviews()
    """
    def setUp(self):
        self.comments = []
        self.business_list = []
        self.success_user = User('ptah', 'pndungu54@gmail.com', 
        'pass123', 'pass123')        
        self.mock_business = Business("James Barber", "We sell bananas", \
        "fruit vendors", "Kawangware", "1234-Kawangware", self.success_user.name)
        # self.mock_business.create_business(self.business_list)

    def tearDown(self):        
        del self.mock_business
        del self.success_user
        del self.business_list

    def test_create_business(self):
        """Test whether a business can be created succesfully"""
        original_length = len(self.business_list)
        self.mock_business.create_business(self.business_list)
        self.assertEqual(original_length + 1, len(self.business_list))

    def test_cannot_create_duplicate_businesses(self):
        """Test app cannot duplicate business"""
        original_length = len(self.business_list)
        self.mock_business.create_business(self.business_list)    
        original_length = len(self.business_list)
        self.mock_business.create_business(self.business_list)
        self.assertEqual(original_length, len(self.business_list))          
        
    
    def test_edit_business(self):
        """Test app can edit a business successfully"""
        self.mock_business.create_business(self.business_list)  
        res = self.mock_business.edit_business(self.business_list, 
        Description='We no longer sell bananas', Location='Somewhere')
        self.assertIn('We no longer sell bananas', 
        self.business_list[0]['Description'])
        self.assertIn('Somewhere', self.business_list[0]['Location'])
        
        
    def test_delete_business(self):
        """Test app can delete business successfully"""
        self.mock_business.create_business(self.business_list)  
        response = Business.delete_business(self.business_list, 1)
        self.assertTrue(response)
        self.assertEqual(Business.get_all_businesses(self.business_list), [])
    
    def test_find_event_by_id(self):
        """Test app can find a business by id"""
        self.mock_business.create_business(self.business_list)
        response = Business.get_business_by_id(self.business_list, 1)
        print(response)
        self.assertIn('James Barber', response['Name'])
        
        
    def test_find_businesses_by_category(self):
        """Test app can find a businesses by category"""
        self.mock_business.create_business(self.business_list)  
        response = Business.get_businesses_by_category(self.business_list,
        'fruit vendors')
        self.assertIn('James Barber', response[0]['Name'])

    def test_find_businesses_by_location(self):
        """Test app can find a businesses by Location"""
        self.mock_business.create_business(self.business_list)                  
        response = Business.get_businesses_by_location(self.business_list, 
        'Kawangware')
        self.assertIn('James Barber', response[0]['Name'])

    def test_add_business_review(self):
        """Test user can write a business review"""
        self.mock_business.create_business(self.business_list)
        response = self.mock_business.write_review('Loved the place', 
        self.success_user.name)
        self.assertEqual(response['message'], 'Review written successfuly')

    def test_get_all_reviews(self):
        """Test app can get all reviews for a particular business"""
        self.mock_business.create_business(self.business_list)        
        self.mock_business.write_review('Worst services ever', 
        self.success_user.name)
        initial_length = len(self.mock_business.reviews)
        self.mock_business.write_review('Impunity of the highest order', 
        self.success_user.name)
        self.assertEqual(initial_length + 1, 2)
    