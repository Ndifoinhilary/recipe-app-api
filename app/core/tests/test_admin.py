from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()
class TestAdminSite(TestCase):
    """
    Test the admin site
    """
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email="testadmin@example.com",
            password="adminpassword",
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testuserpassword",
            name="testuser",
        )


    def test_users_listed(self):
        """
        Test that the users are listed on the user page
        :return:
        """
        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
