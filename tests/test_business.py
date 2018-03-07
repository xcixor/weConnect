"""Contains test for the Business class"""

import unittest

from app.api_v1.models import Business, User

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
        self.mock_business = Business("James Barber", "We sell bananas", \
        "fruit vendors", "Kawangware", "1234-Kawangware")
        
        self.success_user = User('ptah', 'pndungu54@gmail.com', 'pass123', 'pass123')
        
    
        # for business in self.mock_business.businesses:
        #     self.mock_business.businesses.remove(business)

    def test_create_business(self):
        """Test whether a business can be created succesfully"""
        response = self.mock_business.create_business()
        self.assertTrue(response)
        self.assertEqual(Business.get_all_businesses(), \
        [{"Id":1, "Name":"James Barber", "Description":"We sell bananas", \
        "Location":"Kawangware", "Category":"fruit vendors", "Address":"1234-Kawangware", "Reviews":[]}])


    def test_cannot_create_duplicate_businesses(self):
        """Test app cannot duplicate business"""
        self.mock_business.create_business()
        response = self.mock_business.create_business()
        self.assertEqual(response['message'], \
        'Cannot create duplicate business')
      
        
    
    def test_edit_business(self):
        """Test app can edit a business successfully"""
        print(self.mock_business.create_business())
        response = self.mock_business.edit_business(Description='We no longer sell bananas', Location='Somewhere')
        self.assertTrue(response)
        self.assertEqual(Business.get_all_businesses(), \
        [{"Id":1, "Name":"James Barber", "Description":"We no longer sell bananas", \
        "Location":"Somewhere", "Category":"fruit vendors", "Address":"1234-Kawangware", "Reviews":[]}])
 
        
    def test_delete_business(self):
        """Test app can delete business successfully"""
        self.mock_business.create_business()
        response = self.mock_business.delete_business()
        self.assertTrue(response)
        self.assertEqual(Business.get_all_businesses(), [])
    
        

    def test_find_event_by_id(self):
        """Test app can find a business by id"""
        self.mock_business.create_business()
        response = Business.get_business_by_id(1)
        self.assertEqual(response, {"Id":1, "Name":"James Barber", "Description":"We sell bananas", "Location":"Kawangware", "Category":"fruit vendors", "Address":"1234-Kawangware", "Reviews":[]})
        
    def test_find_businesses_by_category(self):
        """Test app can find a businesses by category"""
        self.mock_business.create_business()
        another_biz = Business("jane's fruits", \
        "All kinds of fruits", "Kihanya", "fruit vendors")
        another_biz.create_business()
        response = Business.get_businesses_by_category()
        self.assertEqual(response, [{"Name":"James Barber", \
        "Description":"We sell bananas", "Location":"Kawangware", \
        "Category":"fruit vendors"},
        {"Name":"jane's fruits", "Description":"All kinds of fruits", \
        "Location":"Kihanya", "Category":"fruit vendors"}])

    def tearDown(self):
        del self.mock_business

    # def test_find_businesses_by_location(self):
    #     """Test app can find a businesses by category"""
    #     self.mock_business.create_business()
    #     another_biz = Business("juma cafe", "Mandazi moto stop", \
    #     "Kawangware", "food")
    #     another_biz.create_business()
    #     response = Business.get_businesses_by_category()
    #     self.assertEqual(response, [{"Name":"James Barber", \
    #     "Description":"We sell bananas", "Location":"Kawangware", \
    #     "Category":"fruit vendors"},
    #     {"Name":"juma cafe", "Description":"Mandazi moto stop", \
    #     "Location":"Kawangware", "Category":"food"}])
        

    # def test_add_business_review(self):
    #     """Test user can write a business review"""
    #     self.mock_business.create_business()
    #     response = self.mock_business.write_review('Loved the place', \
    #     self.success_user.username)
    #     self.assertEqual(response, 'Review written successfuly')

    # def test_get_all_reviews(self):
    #     """Test app can get all reviews for a particular business"""
    #     self.mock_business.create_business()
    #     self.mock_business.write_review('Worst services ever')
    #     self.mock_business.write_review('Impunity of the highest order', \
    #     self.success_user.username)
    #     response = self.mock_business.get_all_reviews()
    #     self.assertEqual(response, [{'id':'1', \
    #     'comment':'Worst services ever', 'owner':'ptah'}, \
    #     {'id':'2', 'comment':'Impunity of the highest order', \
    #     'owner':'ptah'}])
    