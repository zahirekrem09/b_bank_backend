from rest_framework import serializers
from .models import Ticket
from authentication.serializers import UserTicketOwnerSerializer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer()
    # pro_company_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro",
                  "appointment_date", "feedback_client")
