from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """
    Create and return a test user
    :param params:
    :return: User object
    """

    return get_user_model().objects.create_user(**params)



class PublicUserApiTests(TestCase):
    """
    Test the public user API
    """

    def setUp(self):
        self.client = APIClient()


    def test_create_user_success(self):
        """
        Test creating user with valid payload
        :return:
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'testname',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)


    def test_create_user_already_exists(self):
        """
        Test creating user that already exists
        :return:
        """

        payload = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'testname',
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_for_user(self):
        """
        Test that a token is created for the user
        :return:
        """
        user_details = {
            'email': 'test@example.com',
            'password': 'passwordnow',
            'name': 'testname',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created if invalid credentials are given
        :return:
        """
        create_user(email='test@example.com', password='password')
        payload = {
            'email': 'example.com',
            'password': 'password',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


    def test_create_token_blank_password(self):
        """
        Test that token is not created if password is blank
        :return:
        """

        response = self.client.post(TOKEN_URL, {'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users
        :return:
        """
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class PrivateUserApiTests(TestCase):
    """
    Test the private user API
    """

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password',
            name='testname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user
        :return:
        """

        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_update_user_profile(self):
        """
        Test updating user profile
        :return:
        """

        payload = {
            'name':'new name',
            'password':'newpassword',
        }
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)