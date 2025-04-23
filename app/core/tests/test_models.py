"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelTests(TestCase):
    """
    Test models
    """
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        email = 'test@example.com'
        password = 'test@123'
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_without_email(self):
        """
        Test creating a new user with no email raises error
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='test!2424f')