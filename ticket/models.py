from django.db import models
from authentication.models import User


class Ticket(models.Model):
    owner = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField()
    ticket_received = models.BooleanField(default=False)
    connector = models.CharField(max_length=50, blank=True, null=True)
    pro = models.CharField(max_length=50, blank=True, null=True)
    distance = models.IntegerField(default=0)
    date_sent_client = models.DateTimeField()
    date_sent_pro = models.DateTimeField()
    feedback_client = models.TextField(blank=True, null=True)
    feedback_pro = models.TextField(blank=True, null=True)
    comments_connector = models.TextField(blank=True, null=True)
