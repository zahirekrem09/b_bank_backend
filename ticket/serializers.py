from rest_framework import serializers
from .models import Ticket
from authentication.serializers import UserTicketOwnerSerializer


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
