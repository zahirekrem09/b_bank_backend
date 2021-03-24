import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


def user_directory_path(instance, filename):
    return 'profil_images/{0}/{1}'.format(instance.id, filename)


class UserManager(BaseUserManager):

    def create_user(self, username,  email, first_name, last_name, gdpr_consent, phone_number, password=None, **extra):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email), first_name=first_name, last_name=last_name, phone_number=phone_number, gdpr_consent=gdpr_consent)
        user.set_password(password,)
        # user.is_client = True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password,)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_prouser(self, username,  email, first_name, last_name, zip_address, phone_number, about_me, company_name, for_gender, reserved_capacity, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email), first_name=first_name, last_name=last_name, zip_address=zip_address, phone_number=phone_number, about_me=about_me, company_name=company_name, for_gender=for_gender, reserved_capacity=reserved_capacity)
        user.set_password(password,)
        user.is_pro = True
        user.save()
        return user

    def create_connectoruser(self, username,  email, first_name, last_name, zip_address, phone_number, about_me, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username,
                          email=self.normalize_email(email), first_name=first_name, last_name=last_name, zip_address=zip_address, phone_number=phone_number, about_me=about_me)
        user.set_password(password,)
        user.is_client = True
        user.save()
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
    SERVICE_TYPE_KAPPER = 0
    SERVICE_TYPE_SCHOONHEIDSSPECIALISTE = 1
    SERVICE_TYPE_PEDICURE = 2
    SERVICE_TYPE_VISAGIST = 3
    SERVICE_TYPE_STYLISTE = 4
    SERVICE_TYPE_NAGELSTYLISTE = 5
    SERVICE_TYPE_HAARWERKEN = 6
    SERVICE_TYPE_NOT_SPECIFIED = 7

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
    SERVICE_TYPE_CHOICES = (
        (SERVICE_TYPE_KAPPER, 'kapper'),
        (SERVICE_TYPE_SCHOONHEIDSSPECIALISTE, 'schoonheidsspecialiste'),
        (SERVICE_TYPE_PEDICURE, 'pedicure'),
        (SERVICE_TYPE_VISAGIST, 'visagist'),
        (SERVICE_TYPE_STYLISTE, 'styliste'),
        (SERVICE_TYPE_NAGELSTYLISTE, 'nagelstyliste'),
        (SERVICE_TYPE_HAARWERKEN, 'haarwerken'),
        (SERVICE_TYPE_NOT_SPECIFIED, 'not specified'),

    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 default=GENDER_NOT_SPECIFIED)
    address = models.CharField(max_length=300,  blank=True, null=True)
    zip_address = models.CharField(max_length=8)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    service_type = models.IntegerField(choices=SERVICE_TYPE_CHOICES,
                                       default=SERVICE_TYPE_NOT_SPECIFIED)
    for_gender = models.IntegerField(choices=GENDER_CHOICES,
                                     default=GENDER_NOT_SPECIFIED)
    schedule_for_client = models.DateTimeField(auto_now=True)
    schedule_for_connector = models.DateTimeField(auto_now=True)
    reserved_capacity = models.IntegerField(default=0)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True, null=True)
    twitter_account = models.URLField(max_length=300, blank=True, null=True)
    instagram_account = models.URLField(max_length=300, blank=True, null=True)
    facebook_account = models.URLField(max_length=300, blank=True, null=True)
    youtube_account = models.URLField(max_length=300, blank=True, null=True)
    about_me = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transportation_type = models.IntegerField(
        choices=TRANS_CHOICES, default=TRANS_NOT_SPECIFIED)
    preferred_lang = models.IntegerField(
        choices=PREFERREND_LANG_CHOICES, default=PREFERREND_LANG_NOT_SPECIFIED)
    expectation = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to=user_directory_path, default='default-avatar-icon.png')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_gray = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_connector = models.BooleanField(default=False)
    gdpr_consent = models.BooleanField(default=False)
    #min_incomer = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'first_name', 'zip_address','about_me']
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("created_at",)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# https://tech.serhatteker.com/post/2020-01/uuid-primary-key/
# class ModelUsingUUID(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
