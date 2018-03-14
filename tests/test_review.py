"""Contains tests for the review class"""

import unittest

from app.api_1_0.models import Review, User

class TestReviewCase(unittest.TestCase):
    """Test Review class functionality
    test_create_review()
    test_delete_review()
    test_valid_review()
    """
    def setUp(self):
        self.success_user = User('ptah', 'pndungu54@gmail.com', 
        'pass123', 'pass123')        
        self.review = Review('I didn\'t like your place', 
        self.success_user.name)    
        self.reviews = []            

    def tearDown(self):
        del self.review

    def test_create_review(self):
        """Test app can create review"""
        response = self.review.create_review(self.reviews)
        self.assertEqual(response, {'Id':1, 'Comment':'I didn\'t like your place',
        'Owner':'ptah'})
