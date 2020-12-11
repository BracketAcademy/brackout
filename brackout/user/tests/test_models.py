from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

import datetime as dt


def create_user(email, password, **kwargs):
    return get_user_model().objects.create_user(
        email, password, **kwargs
    )


class TestUser(TestCase):
    ''' Customized User Model Test Case '''

    def test_create_user_with_email(self):
        ''' Test that user is created with valid email '''
        with self.assertRaises(ValueError):
            create_user(
                email=None,
                password='test123'
            )

    def test_create_user(self):
        ''' Test that user is created successfuly '''
        email = 'test@gmail.com'
        password = 'test123'
        test_user = create_user(
            email=email,
            password=password
        )

        self.assertEqual(test_user.email, email)
        self.assertTrue(test_user.check_password(password))
        self.assertTrue(test_user.date_joined)

    def test_email_is_normilized(self):
        ''' Test that normalization of email is ok '''
        email = 'test@GMAIL.com'
        test_user = create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(test_user.email, email.lower())

    def test_create_superuser(self):
        ''' Test creating superuser '''
        test_user = get_user_model().objects.create_superuser(
            email='t@g.com',
            password='test123'
        )

        self.assertTrue(test_user.is_staff)
        self.assertTrue(test_user.is_superuser)

    def test_user_age(self):
        """ Test that user's age is calculated correctly """
        test_user = create_user(
            email='test@gmail.com',
            password='test123',
        )
        test_user.birth_date = dt.date(2000, 1, 1)

        age = timezone.now().date() - test_user.birth_date

        self.assertEqual(
            age.days/365,
            test_user.get_age()
        )

    def test_is_joined_recently_past(self):
        """Test user is joined more than a day"""
        test_user = create_user('test@gmail.com', 'test123')
        test_user.date_joined -= dt.timedelta(days=1, seconds=1)

        self.assertFalse(test_user.is_joined_recently())

    def test_is_joined_recently(self):
        """Test user is joined recently"""
        test_user = create_user('test@gmail.com', 'test123')
        test_user.date_joined -= dt.timedelta(
            hours=23, minutes=59, seconds=59
        )

        self.assertTrue(test_user.is_joined_recently())

    def test_is_joined_recently_future(self):
        """Test user will join in future"""
        test_user = create_user('test@gmail.com', 'test123')
        test_user.date_joined += dt.timedelta(
            days=1, seconds=1
        )

        self.assertFalse(test_user.is_joined_recently())

    def test_get_gender(self):
        """Test the get gender func"""
        test_user = create_user('test@gmail.com', 'test123')
        
        test_user.gender = 'MA'
        self.assertEqual(test_user.get_gender(), 'Male')

        test_user.gender = 'FE'
        self.assertEqual(test_user.get_gender(), 'Female')

        test_user.gender = 'NS'
        self.assertEqual(test_user.get_gender(), 'Prefer Not to Say')

        test_user.gender = 'NB'
        self.assertEqual(test_user.get_gender(), 'Non Binary')

        test_user.gender = ''
        self.assertEqual(test_user.get_gender(), None)
