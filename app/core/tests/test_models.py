"""
Test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

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



    def test_create_recipe(self):
        """
        Test creating a new recipe is successful
        :return:
        """
        user = User.objects.create_user(
            email='test@example.com',
            password='password'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('23.00'),
            description='Test Description',
        )
        self.assertEqual( str(recipe),  recipe.title)
        self.assertEqual(recipe.time_minutes, 5)