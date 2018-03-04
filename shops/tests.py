from rest_framework.test import APITestCase
from django.urls import include, path
from django.test import TestCase


class AccountTests(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    """
     As a User (or Administrator), I can sign up using my email & password
    """
    def test_create_account(self):
        self.assertEqual(1, 0)

    """
    As an Administrator, I can promote other users to administrator
    """
    def test_promote_user_as_admin(self):
        self.assertEqual(1, 0)

    def test_promote_user_as_user(self):
        # test that a normal user cannot promote. 403 response
        self.assertEqual(1, 0)


class LoginTests(TestCase):
    """
    As a User (or Administrator), I can sign in using my email & password
    """
    def test_login(self):
        response = self.client.get('/login/')
        self.assertRedirects(response, '/accounts/login/?next=/shops/')

    """
    When I load the main page without logging in, I am redirected to
    the login page
    """
    def test_anonymous_redirected_to_login_page(self):
        self.assertEqual(1, 0)


class ShopsTests(APITestCase):
    """
    As an Administrator, I can load shops to the database,
    from an uploaded json file (shops.json provided).
    """
    def test_admin_can_upload_shops(self):
        self.assertEqual(1, 0)

    def test_user_cannot_upload_shops(self):
        self.assertEqual(1, 0)

    """
    As a User (or Administrator), I can display the list of shops
    """
    def test_any_user_can_list_shops(self):
        self.assertEqual(1, 0)

    """
    As a User, I can like a shop, so it can be added to my preferred shops
    """
    def test_any_user_can_like_shop(self):
        self.assertEqual(1, 0)

    """
    Acceptance criteria: liked shops shouldn’t be displayed on the main page
    """
    def test_liked_shops_not_in_main_list(self):
        self.assertEqual(1, 0)

    """
    As a User, I can display the list of preferred shops
    """
    def test_user_retrieve_preferred_shops(self):
        self.assertEqual(1, 0)

    """
    As a User, I can remove a shop from my preferred shops list
    """
    def test_user_delete_preferred_shop(self):
        self.assertEqual(1, 0)
