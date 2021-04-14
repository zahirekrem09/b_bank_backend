from django.db import models
from authentication.models import User


# def user_directory_path(instance, filename):
#     return 'ticket/{0}/{1}'.format(instance.owner.id, filename)
class Ticket(models.Model):
    SERVICE_TYPE_KAPPER = 0
    SERVICE_TYPE_SCHOONHEIDSSPECIALISTE = 1
    SERVICE_TYPE_PEDICURE = 2
    SERVICE_TYPE_VISAGIST = 3
    SERVICE_TYPE_STYLISTE = 4
    SERVICE_TYPE_NAGELSTYLISTE = 5
    SERVICE_TYPE_HAARWERKEN = 6
    SERVICE_TYPE_NOT_SPECIFIED = 7
    AREA_ZERO = 0
    AREA_ONE = 1
    AREA_NOT_SPECIFIED = 2
    AREA_CHOICES = (
        (AREA_ZERO, "Amsterdam"),
        (AREA_ONE, "Rodertam"),
        (AREA_NOT_SPECIFIED, "not specified"),
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
    owner = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True, null=True)
    about_me = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    area = models.IntegerField(choices=AREA_CHOICES,
                               default=AREA_NOT_SPECIFIED)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    ticket_received = models.BooleanField(default=False)
    connector = models.PositiveIntegerField(blank=True, null=True)
    pro = models.PositiveIntegerField(blank=True, null=True)
    service_type = models.IntegerField(choices=SERVICE_TYPE_CHOICES,
                                       default=SERVICE_TYPE_NOT_SPECIFIED)
    distance = models.IntegerField(default=0)
    terms_approved = models.BooleanField(default=False)
    is_pro_confirm = models.BooleanField(default=False)
    is_client_confirm = models.BooleanField(default=False)
    is_intake_call = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    intake_call_date = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return self.email

    class Meta:
        ordering = ("created_at", "is_intake_call", "updated_at",)


class Feedback(models.Model):
    owner = models.ForeignKey(
        User, related_name='feedbacks', on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket, related_name='feedbacks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1500)

    class Meta:
        ordering = ("created_at",)


class FeedBackImage(models.Model):
    image = models.ImageField(upload_to='feedbacks_images')
    feedback = models.ForeignKey(
        Feedback, on_delete=models.CASCADE, null=True, related_name='feedback_images')
