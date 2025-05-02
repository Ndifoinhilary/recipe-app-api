from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe,Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailsSerializer


RECIPE_URL = reverse('recipe:recipe-list')

def create_user(**params):
    """"
    Create a new user with given details
    """
    return get_user_model().objects.create(**params)

def recipe_details(recipe_id):
    """
    Return recipe data
    :param recipe_id:
    :return:
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """
    Create a new recipe with given details
    :param user:
    :param params:
    :return:
    """
    defaults = {
        'title': 'Test Recipe',
        'time_minutes': 10,
        'price': Decimal('10.00'),
        'description': 'Test Recipe',
        'link': 'http://test.com',
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """
    Test the publicly available recipe API
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required
        :return:
        """
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test the private recipe API
    """
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password',
            name='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_recipes(self):
        """
        Test retrieving a list of recipes
        :return:
        """
        create_recipe(self.user)
        create_recipe(self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_recipe_limited_to_user(self):
        """
        Test that recipes returned are for the authenticated user
        :return:
        """
        user2 = create_user(
            email='test2@example.com',
            password='password',
        )
        create_recipe(user=user2)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_view_recipe_detail(self):
        """
        Test viewing a recipe detail
        :return:
        """
        recipe = create_recipe(self.user)
        url = recipe_details(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailsSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_recipe_successful(self):
        """
        Test creating a new recipe
        :return:
        """
        payload = {
            'title': 'Test Recipe',
            'time_minutes': 10,
            'price': Decimal('10.00'),
            'description': 'Test Recipe',
            'link': 'http://test.com',        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_create_recipe_invalid(self):
        """"
        Test creating a new recipe with invalid payload
        """
        payload = {
            'time_minutes': 10,
            'price': Decimal('10.00'),
            'description': 'Test Recipe',
            'link': 'http://test.com',
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_recipe(self):
        """
        Test deleting a recipe
        :return:
        """
        recipe = create_recipe(self.user)
        url = recipe_details(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


    def test_create_recipe_with_ingredients(self):
        """
        Test creating a new recipe with ingredients
        :return:
        """
        payload = {
            'title': 'Test Recipe',
            'time_minutes': 10,
            'price': Decimal('10.00'),
            'description': 'Test Recipe',
            'link': 'http://test.com',
            "ingredients": [{'name':"ingredient1"}, {'name': "test2"}],
        }
        res = self.client.post(RECIPE_URL, payload, format='json')
        recipe = Recipe.objects.filter(user=self.user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for ingredient in payload['ingredients']:
            exists = Ingredient.objects.filter(name=ingredient['name'], user=self.user).exists()
            self.assertTrue(exists)


