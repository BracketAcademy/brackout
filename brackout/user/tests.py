from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


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


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            'admin@gmail.com',
            'admin123'
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test123',
            name='Test user full name'
        )

    def test_users_listed(self):
        ''' Test that users are listed on user page '''
        url = reverse('admin:user_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        ''' User edit page works '''
        url = reverse('admin:user_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        ''' Test that the add user page works '''
        url = reverse('admin:user_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
