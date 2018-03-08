from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from webchallenge.settings import BASE_DIR
from rest_framework import status
from shops.models import Shop
from djet import assertions
import json


User = get_user_model()
users = {
    'admin': {
        'password': 'insecure',
        'email': 'admin@example.com',
        'is_superuser': True
    },
    'gerald': {
        'password': 'notsecure',
        'email': 'gerald@mcfred.com',
    },
    'penelope': {
        'password': 'birdsncatsnbbq!',
        'email': 'penelope@awexome.com',
    }
}


def create_user(**kwargs):
    data = {
        'password': 'secret',
        'email': 'gerald.mcfred@booya.com',
        'is_superuser': False,
    }
    data.update(kwargs)
    user = get_user_model().objects.create_user(**data)
    user.raw_password = data['password']
    return user


class CreateAccountTests(APITestCase,
                         assertions.StatusCodeAssertionsMixin,
                         assertions.InstanceAssertionsMixin):
    """
     As a User (or Administrator), I can sign up using my email & password
    """
    def test_create_user_account(self):
        data = users['gerald']

        response = self.client.post('/shops/auth/users/create/', data)

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertEqual(False, response.data['is_superuser'])
        self.assert_instance_exists(User, email=data['email'])
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_create_admin_account(self):
        data = users['admin']

        response = self.client.post('/shops/auth/users/create/', data)

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertEqual(True, response.data['is_superuser'])
        self.assert_instance_exists(User, email=data['email'])
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))


class LoginTests(APITestCase,
                 assertions.StatusCodeAssertionsMixin,
                 assertions.InstanceAssertionsMixin):
    def setUp(self):
        for _, userdata in users.items():
            create_user(**userdata)

    """
    As a User (or Administrator), I can sign in using my email & password
    """
    def test_user_login(self):
        data = users['gerald']

        response = self.client.post('/shops/auth/token/create/', data)

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)
        token_string = 'Token {}'.format(response.data['auth_token'])

        auth_response = self.client.get("/shops/auth/me/",
                                        HTTP_AUTHORIZATION=token_string)

        self.assert_status_equal(auth_response, status.HTTP_200_OK)
        self.assertEqual(data['email'], auth_response.data['email'])

    def test_admin_login(self):
        data = users['admin']

        response = self.client.post('/shops/auth/token/create/', data)

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)
        token_string = 'Token {}'.format(response.data['auth_token'])

        auth_response = self.client.get("/shops/auth/me/",
                                        HTTP_AUTHORIZATION=token_string)

        self.assert_status_equal(auth_response, status.HTTP_200_OK)
        self.assertEqual(data['email'], auth_response.data['email'])


class PromoteUserTests(APITestCase,
                       assertions.StatusCodeAssertionsMixin,
                       assertions.InstanceAssertionsMixin):

    @classmethod
    def setUpClass(self):
        super(PromoteUserTests, self).setUpClass()

        for _, userdata in users.items():
            create_user(**userdata)

        pk = User.objects.get(email=users['penelope']['email']).pk
        penelope_data = users['penelope'].copy()
        penelope_data.update({'is_superuser': True})
        self._penelope = {
            'data': penelope_data,
            'url': '/shops/api/users/{}/'.format(pk),
        }

    def get_token(self, user):
        response = self.client.post('/shops/auth/token/create/', user)
        token_string = 'Token {}'.format(response.data['auth_token'])
        return token_string

    """
    As an Administrator, I can promote other users to administrator
    """
    def test_promote_user_as_admin(self):
        admin = users['admin']
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token(admin))
        response = self.client.patch(self._penelope['url'],
                                     {'is_superuser': True})

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertEqual(response.data['is_superuser'], True)

    """
    As a User, I cannot promote other users to administrator
    """
    def test_promote_user_as_user(self):
        gerald = users['gerald']
        self.client.credentials(HTTP_AUTHORIZATION=self.get_token(gerald))

        response = self.client.patch(self._penelope['url'],
                                     {'is_superuser': True})

        self.assert_status_equal(response, status.HTTP_403_FORBIDDEN)

    """
    Not logged in, I cannot promote other users to administrator
    """
    def test_promote_user_as_anonymous(self):
        response = self.client.patch(self._penelope['url'],
                                     {'is_superuser': True})

        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)


class CreateShopsTests(APITestCase,
                       assertions.StatusCodeAssertionsMixin,
                       assertions.InstanceAssertionsMixin):
    @classmethod
    def setUpClass(self):
        super(CreateShopsTests, self).setUpClass()

        for _, userdata in users.items():
            create_user(**userdata)

        shops_path = BASE_DIR + '/shops/fixtures/shops/shops.json'
        self._shops_list = json.load(open(shops_path))

    def admin_upload_shops(self):
        admin = User.objects.get(email=users['admin']['email'])
        self.client.force_authenticate(user=admin)
        response = self.client.post('/shops/api/shops/', self._shops_list)
        return response

    """
    As an Administrator, I can load shops to the database,
    from an uploaded json file (shops.json provided).
    """
    def test_admin_can_upload_shops(self):
        response = self.admin_upload_shops()
        self.assert_status_equal(response, status.HTTP_201_CREATED)

    def test_admin_upload_clobbers_existing(self):
        posted = self.admin_upload_shops()
        retrieved = self.client.get('/shops/api/shops/')
        self.assertEqual(posted.data, retrieved.data)

    def test_user_cannot_upload_shops(self):
        gerald = User.objects.get(email=users['gerald']['email'])
        self.client.force_authenticate(user=gerald)
        response = self.client.post('/shops/api/shops/', self._shops_list)
        self.assert_status_equal(response, status.HTTP_403_FORBIDDEN)


class ListAndLikeShopsTests(APITestCase,
                            assertions.StatusCodeAssertionsMixin,
                            assertions.InstanceAssertionsMixin):
    @classmethod
    def setUpClass(self):
        super(ListAndLikeShopsTests, self).setUpClass()
        self._shop = Shop.objects.create(title="I'm a shop")
        self._fav_shop = Shop.objects.create(title="I'm a favorited shop")

        self._admin = create_user(**users['admin'])
        self._gerald = create_user(**users['gerald'])

    """
    As a User (or Administrator), I can display the list of shops
    """
    def test_any_user_can_list_shops(self):
            self.client.force_authenticate(self._gerald)
            response = self.client.get('/shops/api/shops/')
            self.assert_status_equal(response, status.HTTP_200_OK)

            self.client.force_authenticate(self._admin)
            response = self.client.get('/shops/api/shops/')
            self.assert_status_equal(response, status.HTTP_200_OK)

    """
    As a User, I can like a shop, so it can be added to my preferred shops
    """
    def test_any_user_can_like_shop(self):
        self.client.force_authenticate(self._gerald)
        pk = self._fav_shop.pk
        liked_shop_url = '/shops/api/shops/{}/like/'.format(pk)
        response = self.client.put(liked_shop_url)

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assert_instance_exists(Shop, users=self._gerald)

    """
    Acceptance criteria: liked shops shouldn’t be displayed on the main page
    """
    def test_liked_shops_not_in_main_list(self):
        self.client.force_authenticate(self._gerald)
        self._fav_shop.users.add(self._gerald)
        self._fav_shop.save()
        response = self.client.get('/shops/api/shops/')
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertNotContains(response, "I'm a favorited shop")

    """
    As a User, I can display the list of preferred shops
    """
    def test_user_retrieve_preferred_shops(self):
        self.client.force_authenticate(self._gerald)
        url = '/shops/api/users/{}/shops/'.format(self._gerald.pk)
        response = self.client.get(url)
        self.assert_status_equal(response, status.HTTP_200_OK)

    """
    As a User, I can remove a shop from my preferred shops list
    """
    def test_user_unlike_shop(self):
        self.client.force_authenticate(self._gerald)
        pk = self._fav_shop.pk
        unliked_shop_url = '/shops/api/shops/{}/unlike/'.format(pk)
        response = self.client.put(unliked_shop_url)
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assert_instance_does_not_exist(Shop, users=self._gerald)
