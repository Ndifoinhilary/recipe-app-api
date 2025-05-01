"""
Test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

User = get_user_model()

def create_user():
    """
    Create a user
    :return:
    """
    return User.objects.create_user(email='test@exmaple.com', password='password')


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


    def test_create_tag(self):
        """"
        Test creating a new tag is successful
        """
        user = create_user()
        tags = models.Tag.objects.create(name='Test Tag', user=user)
        self.assertEqual( str(tags), tags.name)


    def test_create_ingredient(self):
        """
        Test creating a new ingredient is successful
        :return:
        """
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Test Ingredient',
        )
        self.assertEqual( str(ingredient), ingredient.name)