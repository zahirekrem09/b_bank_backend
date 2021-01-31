from django.db import models
from authentication.models import User


class Ticket(models.Model):
   # TODO: tickete göre değişicek
    owner = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20, blank=True, null=True)
    about_me = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    ticket_received = models.BooleanField(default=False)
    connector = models.PositiveIntegerField(blank=True, null=True)
    pro = models.PositiveIntegerField(blank=True, null=True)
    distance = models.IntegerField(default=0)
    terms_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email
