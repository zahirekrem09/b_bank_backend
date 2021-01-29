from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Ticket
from authentication.serializers import UserTicketOwnerSerializer
from authentication.models import User


class Pro(serializers.PrimaryKeyRelatedField):

    def display_value(self, instance):
        return instance.username


class TicketSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "owner",
                  "feedback_client")


class TicketConnectorDetailSerializer(serializers.ModelSerializer):
    pro = Pro(queryset=User.objects.filter(is_pro=True))
    connector = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro", "connector",
                  "appointment_date", "feedback_client", "comments_connector")

    def get_connector(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if obj.connector == request.user.username:
                return True
            return False
