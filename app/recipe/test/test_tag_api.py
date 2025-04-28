"""
Testing tag api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer
TAG_URL = reverse('recipe:tag-list')


def create_tag(tag_name, user):
    """"
    Create a new tag"""
    tag = Tag.objects.create(name=tag_name, user=user)
    return tag


def tag_details(tag_id):
    """"
    Return tag details
    """
    return reverse('recipe:tag-detail', args=[tag_id])


User = get_user_model()


class PublicTagApiTests(TestCase):
    """
    Test the publicly available tag api
    """

    def setUp(self):
        self.client = APIClient()

    def test_tags_list(self):
        """
        Test retrieving tags list
        :return:
        """
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """
    Test the authorized user tag api
    """

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)


    def test_retrieve_tags(self):
        """
        Test retrieving tags
        :return:
        """
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        """
        Test retrieving tags list
        :return:
        """
        user2 = User.objects.create_user(email='test2@example.com', password='password')
        create_tag("tag1", user=self.user)
        create_tag("tag2", user=self.user)
        create_tag("tag3", user=user2)
        res = self.client.get(TAG_URL)
        user_tags = Tag.objects.filter(user=self.user).order_by('-name')
        serializer = TagSerializer(user_tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



    def test_tags_detail(self):
        """
        Test retrieving tags detail
        :return:
        """
        tag = create_tag("tag3", user=self.user)
        url = tag_details(tag.id)
        res = self.client.get(url)
        serializer = TagSerializer(tag)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)




