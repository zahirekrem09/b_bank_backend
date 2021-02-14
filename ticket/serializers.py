from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import FeedBackImage, Feedback, Ticket
from authentication.serializers import UserTicketOwnerSerializer
from authentication.models import User
from authentication.utils import Util
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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


class TicketClientCreateSerializer(serializers.ModelSerializer):
    service_type = serializers.ChoiceField(choices=Ticket.SERVICE_TYPE_CHOICES)

    class Meta:
        model = Ticket
        fields = ("id", "service_type")


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    service_type = serializers.ChoiceField(choices=Ticket.SERVICE_TYPE_CHOICES)
    appointment_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "owner", "appointment_date", "service_type")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackImage
        fields = ('image', "feedback")


class FeedbackSerializers(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    # ticket = TicketClientDetailSerializer(read_only=True)
    feedback_images = ImageSerializer(many=True)

    class Meta:
        model = Feedback
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    feedbacks = FeedbackSerializers(many=True)
    service_type = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = "__all__"

    def get_service_type(self, obj):
        return obj.get_service_type_display()


class TicketConnectorDetailSerializer(serializers.ModelSerializer):
    pro = serializers.ChoiceField(choices=pro_user_feild())
    connector = serializers.IntegerField(read_only=True)
    service_type = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro", "connector",
                  "appointment_date", 'service_type')

    def get_service_type(self, obj):
        return obj.get_service_type_display()

    def update(self, instance, validated_data):
        request = self.context["request"]
        instance.connector = request.user.id
        instance.pro = request.data.get("pro")
        instance.appointment_date = request.data.get("appointment_date")
        instance.save()
        pro = User.objects.get(id=instance.pro)
        owner = User.objects.get(id=instance.owner.id)
        email_body = 'Hi '+pro.username + \
            ' Ticket İnformations \n' + pro.company_name
        data = {'email_body': email_body, 'to_email': pro.email,
                'email_subject': 'Ticket İnformations'}

        subject, from_email = 'Ticket Detail ', 'bbankdummymail@gmail.com'
        html_content = render_to_string('ticket_detail.html', {'owner': owner, 'pro': pro, "appointment_date": request.data.get("appointment_date")
                                                               })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [
                                     pro.email, owner.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return instance


class FeedbackCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("content",)
