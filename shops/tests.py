from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from djet import assertions, restframework


User = get_user_model()
users = {
    'admin': {
        'username': 'admin',
        'password': 'insecure',
        'email': 'admin@example.com',
        'is_superuser': True,
    },
    'gerald': {
        'username': 'gerald',
        'password': 'notsecure',
        'email': 'gerald@mcfred.com',
    }
}


def create_user(**kwargs):
    data = {
        'username': 'gerald',
        'password': 'secret',
        'email': 'gerald.mcfred@booya.com',
        'is_superuser': False,
        'csrf_token': 'asdf'
    }
    data.update(kwargs)
    user = get_user_model().objects.create_user(**data)
    user.raw_password = data['password']
    return user


class AccountTests(restframework.APIViewTestCase,
                   assertions.StatusCodeAssertionsMixin,
                   assertions.InstanceAssertionsMixin):
    """
     As a User (or Administrator), I can sign up using my email & password
    """
    def test_create_user_account(self):
        data = users['gerald']

        response = self.client.post('/shops/auth/users/create/',
                                    data,
                                    format='json')

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assertTrue('password' not in response.data)
        self.assertEqual(False, response.data['is_superuser'])
        self.assert_instance_exists(User, username=data['username'])
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))

    def test_create_admin_account(self):
        data = users['admin']

        response = self.client.post('/shops/auth/users/create/',
                                    data,
                                    format='json')

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assertTrue('password' not in response.data)
        self.assertEqual(True, response.data['is_superuser'])
        self.assert_instance_exists(User, username=data['username'])
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))

    """
    As a User (or Administrator), I can sign in using my email & password
    """
    def test_user_login(self):
        self.assertEqual(1, 0)

    def test_admin_login(self):
        self.assertEqual(1, 0)

    """
    As an Administrator, I can promote other users to administrator
    """
    def test_promote_user_as_admin(self):
        self.assertEqual(1, 0)

    def test_promote_user_as_user(self):
        # test that a normal user cannot promote. 403 response
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
