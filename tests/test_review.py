"""Contains tests for the review class"""

import unittest

from app.api_v1.modules import Review, User

class TestReviewCase(unittest.TestCase):
    """Test Review class functionality
    test_create_review()
    test_delete_review()
    test_valid_review()
    """
    def setUp(self):
        self.review = Review()
        self.success_user = User('ptah', 'pndungu54@gmail.com', 'pass123', 'pass123')

    def tearDown(self):
        del self.review

    def test_create_review(self):
        """Test app can create review"""
        response = self.review.create_review('I didn\'t like your place', self.success_user.username)
        self.assertEqual(response['message'], 'Review written successfuly')
        
    def test_valid_review(self):
        """Test app only allows valid reviews"""
        response = self.review.create_review('@#$%^%$ @#$%^& ^%$')
        self.assertEqual(response, 'Invalid review text')

    def test_delete_review(self):
        """Test app can delete review"""
        response = self.review.delete_review()
        self.assertTrue(response)