from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    ''' User Model Manager '''

    def create_user(self, email, password=None, **extra_fields):
        ''' Exclusive create user function '''
        if not email:
            raise ValueError('Email MUST be included!')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, **params):
        ''' Exclusive create superuser function '''
        user = self.create_user(email, password, **params)
        user.is_staff = True
        user.is_superuser = True
        user.save(self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ''' Custom User Manager '''
    email = models.EmailField('Email Address', unique=True)
    name = models.CharField(verbose_name='Name', max_length=255)
    date_joined = models.DateTimeField(
                                    verbose_name='Date Joined',
                                    auto_now_add=True)
    provider_choices = [
        ('EM', 'email'),
        ('GO', 'google'),
    ]
    auth_provider = models.CharField(
        verbose_name='Auth Provider',
        max_length=2,
        null=False,
        choices=provider_choices,
        default='email'
    )
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)

    birth_date = models.DateField(
                                verbose_name='Birthday Date',
                                blank=True, null=True)
    gender_choices = [
        ('MA', 'Male'),
        ('FE', 'Female'),
        ('NS', 'Prefer Not to Say'),
        ('NB', 'Non Binary'),
    ]
    gender = models.CharField(
                            verbose_name='Gender',
                            max_length=2,
                            choices=gender_choices,
                            blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    objects = UserManager()

    def age(self):
        """
        Get age of user
        """
        if self.birth_date:
            return (timezone.now().date() - self.birth_date).days//365
        else:
            return None

    def is_joined_recently(self):
        """
        Check if the user has joined recently or not
        """
        return timezone.now()-timezone.timedelta(hours=24) \
                <= self.date_joined \
                <= timezone.now()
