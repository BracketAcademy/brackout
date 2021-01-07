from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from django.conf import settings

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create-user')
TOKEN_URL = reverse('user:create-token')
ME_URL = reverse('user:me')
ALL_USERS_URL = reverse('user:get-all-users')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API public """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful """
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test Testy'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, [res.data['email'],])

        user = get_user_model().objects.get(email=res.data['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertFalse(user.is_active)

    def test_user_exists(self):
        """Test creating user that already exist """
        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
            'name': 'Test Testy'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must be more than five characters """
        payload = {
            'email': 'test@gmail.com',
            'password': 'pa',
            'name': 'Test Testy'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for ther user """
        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
            'name': 'Test Testy'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given """
        create_user(
            email='test@gmail.com',
            password='test123',
            name='Test Testy'
        )
        payload = {
            'email': 'test@gmail.com',
            'password': '123test',
            'name': 'Test Testy'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is note created if user doesn't exist """
        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
            'name': 'Test Testy'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are required """
        res = self.client.post(
            TOKEN_URL,
            {
                'email': 'one',
                'password': '',
                'name': 'Test Testy'
            }
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    '''
    def test_send_activation_email(self):
        """Test sending email for activating acounts"""
        email_subject = 'test subject'
        email_body = 'here is body'
        email_from = 'armanhadi728@gmail.com'
        email_to = ['test@test.com',]
        mail.EmailMessage(
            email_subject,
            email_body,
            email_from,
            email_to
        ).send()

        self.assertEqual(len(mail.outbox), len(email_to))
        self.assertEqual(mail.outbox[0].subject, email_subject)
        self.assertEqual(mail.outbox[0].body, email_body)
        self.assertEqual(mail.outbox[0].from_email, email_from)
        self.assertEqual(mail.outbox[0].to, email_to)
    '''


class PrivateUserApiTest(TestCase):
    """Test Api requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='test123',
            name='Test Testy'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.user.email)
        self.assertEqual(res.data['name'], self.user.name)

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on me url """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user """
        payload = {
            'name': 'new name',
            'password': 'newtest123'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_users(self):
        """Test that staff user can get all users"""
        self.user.is_staff = True
        res = self.client.get(ALL_USERS_URL)
        all_users = get_user_model().objects.order_by('-date_joined')

        self.assertEqual(len(res.data), len(all_users))
        for c,i in enumerate(all_users):
            self.assertEqual(i.email, res.data[c]['email'])
            self.assertEqual(i.name, res.data[c]['name'])
