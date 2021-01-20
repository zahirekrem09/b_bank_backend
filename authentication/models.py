from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email,  password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_NOT_SPECIFIED = 2
    TRANS_BUS = 0
    TRANS_METRO = 1
    TRANS_TAXI = 2
    TRANS_NOT_SPECIFIED = 3
    PREFERREND_LANG_DUTCH = 0
    PREFERREND_LANG_ENG = 1
    PREFERREND_LANG_NOT_SPECIFIED = 2

    GENDER_CHOICES = (
        (GENDER_MALE, 'male'),
        (GENDER_FEMALE, 'female'),
        (GENDER_NOT_SPECIFIED, 'not specified'),
    )

    TRANS_CHOICES = (
        (TRANS_BUS, 'bus'),
        (TRANS_METRO, 'metro'),
        (TRANS_TAXI, 'taxi'),
        (TRANS_NOT_SPECIFIED, 'not specified'),

    )
    PREFERREND_LANG_CHOICES = (
        (PREFERREND_LANG_DUTCH, 'dutch'),
        (PREFERREND_LANG_ENG, 'english'),
        (PREFERREND_LANG_NOT_SPECIFIED, 'not specified'),

    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 default=GENDER_NOT_SPECIFIED)
    address = models.CharField(max_length=300,  blank=True, null=True)
    zip_address = models.CharField(max_length=8)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    phone_number2 = models.CharField(max_length=16, blank=True, null=True)
    about_me = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transportation_type = models.IntegerField(
        choices=TRANS_CHOICES, default=TRANS_NOT_SPECIFIED)
    preferred_lang = models.IntegerField(
        choices=PREFERREND_LANG_CHOICES, default=PREFERREND_LANG_NOT_SPECIFIED)
    expectation = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_gray = models.BooleanField(default=False)
    gdpr_consent = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'first_name', 'zip_address','about_me']
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
