from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import FeedBackImage, Feedback, Ticket
from authentication.serializers import UserTicketOwnerSerializer, UserTicketProSerializer
from authentication.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from django.db.models import Q


# class Pro(serializers.PrimaryKeyRelatedField):

#     def display_value(self, instance):
#         return instance.username

def pro_user_feild():

    if User.objects.filter(is_pro=True).exists():
        pro_user = [(u.id, u.company_name)
                    for u in User.objects.filter(is_pro=True)]
    else:
        pro_user = []

    return pro_user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackImage
        fields = ('image', "feedback")


class FeedbackSerializers(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    # ticket = TicketClientDetailSerializer(read_only=True)
    feedback_images = ImageSerializer(many=True, read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Feedback
        fields = ('id', 'owner', 'ticket', 'feedback_images', 'content')


class TicketClientCreateSerializer(serializers.ModelSerializer):
    # service_type = serializers.ChoiceField(choices=Ticket.SERVICE_TYPE_CHOICES)
    owner = UserTicketOwnerSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "service_type", "owner", "terms_approved")
        read_only_fields = ('owner', 'terms_approved', 'service_type')


class TicketClientDetailSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    # service_type = serializers.ChoiceField(choices=Ticket.SERVICE_TYPE_CHOICES)
    appointment_date = serializers.DateTimeField()

    class Meta:
        model = Ticket
        fields = ("id", "owner", "appointment_date")


# İd ticket id


class TicketSerializer(serializers.ModelSerializer):
    owner = UserTicketOwnerSerializer(read_only=True)
    feedbacks = FeedbackSerializers(many=True)
    service_type = serializers.SerializerMethodField()
    pro_detail = serializers.SerializerMethodField()
    ticket_status = serializers.SerializerMethodField()
    feedback_url = serializers.HyperlinkedIdentityField(
        view_name='feedback',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Ticket
        fields = "__all__"

    def get_service_type(self, obj):
        return obj.get_service_type_display()

    # def get_pro_detail(self, obj):
    #     try:
    #         pro_detail = get_object_or_404(User, pk=obj.pro)
    #         serializer = UserTicketProSerializer(pro_detail)
    #         # print(serializer.data)
    #         return serializer.data
    #     except:
    #         pass

    def get_pro_detail(self, obj):
        try:
            pro_detail = get_object_or_404(User, pk=obj.pro)
            serializer = UserTicketOwnerSerializer(pro_detail)
            # print(serializer.data)
            return serializer.data
        except:
            pass

    def get_ticket_status(self, obj):
        request = self.context['request']
        if(obj.terms_approved == True and obj.pro and obj.appointment_date and obj.appointment_date < timezone.now() and Feedback.objects.filter(ticket=obj, owner=request.user).exists()):
            return "5"
        if(obj.terms_approved == True and obj.pro and obj.appointment_date and obj.appointment_date < timezone.now()):
            return "4"
        elif (obj.terms_approved == True and obj.pro and obj.appointment_date):
            return "3"
        elif(obj.terms_approved == True and obj.pro):
            return "2"
        elif (obj.pro == True):
            return "1"
        else:
            return "0"


class TicketTermsApprovedSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=555544)

    class Meta:
        model = Ticket
        fields = ['id']


class TicketConnectorDetailSerializer(serializers.ModelSerializer):
    # pro = serializers.ChoiceField(choices=pro_user_feild())
    connector = serializers.IntegerField(read_only=True)
    pro = serializers.IntegerField()
    # service_type = serializers.SerializerMethodField()
    service_type = serializers.ChoiceField(choices=Ticket.SERVICE_TYPE_CHOICES)

    class Meta:
        model = Ticket
        fields = ("id", "owner", "pro", "connector",
                  "appointment_date", 'service_type')

        read_only_fields = ('appointment_date', 'owner', 'connector')

    def get_service_type(self, obj):
        return obj.get_service_type_display()

    def update(self, instance, validated_data):
        request = self.context["request"]
        instance.connector = request.user.id
        instance.pro = request.data.get("pro")
        instance.service_type = request.data.get("service_type")
        instance.save()

        if instance.terms_approved == False:
            FRONTEND_URL = "https://beauty-bank-frontend.herokuapp.com/"
            owner = User.objects.get(id=instance.owner.id)

            terms_approved_link = FRONTEND_URL + \
                'terms_approved/' + str(instance.id)
            subject, from_email, to = 'Terms Approved', 'bbankdummymail@gmail.com', owner.email

            html_content = render_to_string('terms_approved_link.html', {
                                            'terms_approved_link': terms_approved_link, 'user': owner, 'ticket': instance})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        # confirm_link = FRONTEND_URL + 'ticket/confirm/' + str(instance.id)
        # pro = User.objects.get(id=instance.pro)
        # owner = User.objects.get(id=instance.owner.id)
        # # email_body = 'Hi '+pro.username + \
        # #     ' Ticket İnformations \n' + pro.company_name
        # # data = {'email_body': email_body, 'to_email': pro.email,
        # #         'email_subject': 'Ticket İnformations'}

        # subject, from_email = 'Ticket Detail ', 'bbankdummymail@gmail.com'
        # html_content = render_to_string('ticket_detail.html', {'owner': owner, 'pro': pro, "appointment_date": request.data.get("appointment_date"), "confirm_link": confirm_link
        #                                                        })
        # text_content = strip_tags(html_content)
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [
        #                              pro.email, owner.email])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        return instance


class FeedbackCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("content",)
        read_only_fields = ("ticket",)
