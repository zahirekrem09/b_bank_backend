from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import FeedBackImage, Feedback, Ticket
from authentication.serializers import UserTicketOwnerSerializer
from authentication.models import User
from authentication.utils import Util


# class Pro(serializers.PrimaryKeyRelatedField):

#     def display_value(self, instance):
#         return instance.username

def pro_user_feild():

    if User.objects.filter(is_pro=True).exists():
        pro_user = [(u.id, u.username)
                    for u in User.objects.filter(is_pro=True)]
    else:
        pro_user = []

    return pro_user


class TicketSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "owner", "appointment_date")


class TicketConnectorDetailSerializer(serializers.ModelSerializer):
    pro = serializers.ChoiceField(choices=pro_user_feild)
    connector = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro", "connector", "appointment_date")

    def update(self, instance, validated_data):
        request = self.context["request"]
        instance.connector = request.user.id
        instance.pro = request.data.get("pro")
        pro = User.objects.get(id=instance.pro)
        owner = User.objects.get(id=instance.owner.id)
        email_body = 'Hi '+pro.username + \
            ' Ticket İnformations \n' + pro.company_name
        data = {'email_body': email_body, 'to_email': pro.email,
                'email_subject': 'Ticket İnformations'}

        Util.send_email(data)

        instance.appointment_date = request.data.get("appointment_date")
        instance.save()
        # print(request.data)
        return instance


class FeedbackCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("content",)


class FeedbackSerializers(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    ticket = TicketClientDetailSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackImage
        fields = ('image',)
