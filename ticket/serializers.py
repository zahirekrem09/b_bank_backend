from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Ticket
from authentication.serializers import UserTicketOwnerSerializer
from authentication.models import User


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    # pro_company_name = serializers.SerializerMethodField()
    pro = serializers.CharField(read_only=True)
    # TODO girilen pro ya göre pronun comp. name eklenecek

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro",
                  "appointment_date", "feedback_client")

class Pro(serializers.PrimaryKeyRelatedField):
    
    def display_value(self, instance):
        return instance.username

class TicketConnectorDetailSerializer(serializers.ModelSerializer):
    # owner = UserTicketOwnerSerializer(read_only=True)
    # pro_company_name = serializers.SerializerMethodField()
    pro = Pro(queryset=User.objects.filter(is_pro=True))
    # TODO girilen pro ya göre pronun comp. name eklenecek

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro",
                  "appointment_date", "feedback_client", "comments_connector")
