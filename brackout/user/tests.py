from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUser(TestCase):
    ''' Customized User Model Test Case '''

    def test_create_user_with_email(self):
        ''' Test that user is created with valid email '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                                                email=None,
                                                password='test123')

    def test_create_user(self):
        ''' Test that user is created successfuly '''
        email = 'test@gmail.com'
        password = 'test123'
        test_user = get_user_model().objects.create_user(
                                                        email=email,
                                                        password=password)

        self.assertEqual(test_user.email, email)
        self.assertTrue(test_user.check_password(password))
        self.assertTrue(test_user.date_joined)

    def test_email_is_normilized(self):
        ''' Test that normalization of email is ok '''
        email = 'test@GMAIL.com'
        test_user = get_user_model().objects.create_user(
                                                        email=email,
                                                        password='test123')

        self.assertEqual(test_user.email, email.lower())

    def test_create_superuser(self):
        ''' Test creating superuser '''
        test_user = get_user_model().objects.create_superuser(
                                                            email='t@g.com',
                                                            password='test123')

        self.assertTrue(test_user.is_staff)
        self.assertTrue(test_user.is_superuser)
