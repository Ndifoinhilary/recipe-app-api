from django.contrib.auth import get_user_model
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

User = get_user_model()

INGREDIENT_URL = reverse('recipe:ingredient-list')


def create_user(**params):
    """
    Create a user for testing
    :param params:
    :return:
    """
    return  User.objects.create_user(**params)


def create_ingredient(**params):
    """
    Create a ingredient for testing
    :param params:
    :return:
    """
    return Ingredient.objects.create(**params)


class PublicIngredientApiTests(TestCase):
    """
    Test the publicly available ingredients API
    """

    def setUp(self):
        self.client = APIClient()

    def test_ingredients_list(self):
        """
        Test ingredients list API
        :return:
        """
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """
    Test the private ingredients API
    """

    def setUp(self):
        self.user = create_user(email='test@example.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_ingredients_list(self):
        """
        Test ingredients list API
        :return:
        """
        create_ingredient(name='test', user=self.user)
        create_ingredient(name='test2', user=self.user)
        create_ingredient(name='test3', user=self.user)
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)