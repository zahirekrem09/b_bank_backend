from django.shortcuts import render, get_object_or_404
from .serializers import (
    TicketSerializer, TicketClientDetailSerializer, TicketConnectorDetailSerializer, ImageSerializer, FeedbackCreateSerializers, FeedbackSerializers, TicketClientCreateSerializer, TicketTermsApprovedSerializer, TicketConnectorIntakeSerializer, TicketClientActiveSerializer)
from .models import FeedBackImage, Feedback, Ticket
from .helpers import modify_input_for_multiple_files
from django.shortcuts import render
from .permission import IsOwner, IsOwnerOrReadOnly
from rest_framework.views import APIView
from authentication.models import User
from authentication.permission import IsConnectorUser
from rest_framework import generics, status, views, permissions, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q, Count, Subquery, OuterRef
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from bbank.pagination import SmallPagination, LargePagination
from django_filters import rest_framework as djfilters
from .filter import TicketFilter
from geopy.distance import geodesic
from decouple import config


class CreateTicketsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TicketClientCreateSerializer

    def post(self, request, **extra):
        serializer = self.serializer_class(data=request.data)
        owner = User.objects.get(username=request.user.username)
        ticket = Ticket.objects.create(owner=owner, email=owner.email,
                                       first_name=owner.first_name, last_name=owner.last_name, phone_number=owner.phone_number, about_me=owner.about_me, ** extra)

        FRONTEND_URL = config('FRONTEND_URL')
        subject, from_email, to = 'Ticket Create Info', config(
            'EMAIL_HOST_USER'), owner.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('ticket_create_info.html', {
                                        'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': owner})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            return Response({'detail': 'Couldn not send email'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(TicketSerializer(ticket, context={'request': request}).data, status=status.HTTP_201_CREATED)


class TicketTermsApprovedView(APIView):
    serializer_class = TicketTermsApprovedSerializer
    queryset = Ticket.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        ticket_id = request.data['id']
        # current_user = User.objects.get(username=request.user.username)
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.terms_approved = True
        ticket.save()

        data = {
            "messages": "Ticket Terms Approved Successfuly"}

        return Response(data, status=status.HTTP_200_OK)


class ConfirmTicketsView(APIView):
    serializer_class = TicketClientDetailSerializer
    queryset = Ticket.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        current_user = User.objects.get(username=request.user.username)
        ticket_id = self.kwargs["id"]
        ticket = Ticket.objects.get(id=ticket_id)
        if(ticket.owner == current_user):
            ticket.is_client_confirm = True
            ticket.save()
        elif (current_user == ticket.pro):
            ticket.is_pro_confirm = True
            ticket.save()
        else:
            return Response({"error": "Not confirm ticket "}, status=400)
        data = {
            "messages": "Confirm  Ticket Successfuly"}

        return Response(data, status=status.HTTP_200_OK)


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = SmallPagination
    queryset = Ticket.objects.all().order_by('-created_at')
    filter_class = TicketFilter
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, djfilters.DjangoFilterBackend,)
    search_fields = ("owner__username", 'email', 'first_name',
                     'last_name', 'company_name')
    # filterset_fields = ['is_gray', 'is_client',
    #                     'is_pro', 'is_sponsor', 'is_connector']
    # ordering_fields = ['is_gray', 'is_client',
    #                    'is_pro', 'is_sponsor', 'is_connector']
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ticket.objects.all().order_by('-created_at')
        if self.request.user.is_pro == True:
            queryset = Ticket.objects.filter(
                pro=self.request.user.id).order_by('-created_at')
            return queryset
        elif self.request.user.is_client == True:
            queryset = Ticket.objects.filter(
                owner=self.request.user).order_by('-created_at')
            return queryset
        else:
            return queryset


class ClientTicketsListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ticket.objects.filter(owner=self.request.user)
        return queryset


class ClientTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketClientDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ticket.objects.filter(owner=self.request.user)
        return queryset


class ConnectorTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketConnectorDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    queryset = Ticket.objects.all()
    lookup_field = 'id'


class ConnectorTicketsIntakeView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketConnectorIntakeSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    queryset = Ticket.objects.all()
    lookup_field = 'id'


class ClientTicketsActiveView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketClientActiveSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

# class FeedBackCreateView(generics.CreateAPIView):
#     queryset = Feedback.objects.all()
#     serializer_class = FeedbackCreateSerializers

#     def perform_create(self, serializer):
#         ticket_pk = self.kwargs.get('ticket_id')
#         ticket = get_object_or_404(Ticket, pk=ticket_pk)
#         serializer.save(owner=self.request.user, ticket=ticket)

# TODO: Sadece kendi ticketi için permisson yazılıcak


"""
Method iki
"""

# Her kullanıcı bir tane feddbacks yapsın


class FeedBackCreateView(APIView):
    # serializer_class = FeedbackSerializers
    permission_classes = (permissions.IsAuthenticated,)
    # queryset = Feedback.objects.all()
    lookup_field = 'id'
    serializer_class = FeedbackCreateSerializers

    def post(self, request, id,  **extra):
        ticket = get_object_or_404(Ticket, id=id)
        # print(ticket.id)
        serializer = FeedbackCreateSerializers(data=request.data)
        if serializer.is_valid():
            # serializer.save(owner=request.user, ticket=ticket)
            qs = Feedback.objects.filter(
                owner=request.user, ticket=ticket)
            if qs.exists():
                qs[0].delete()
            else:
                fed = Feedback.objects.create(
                    owner=request.user, ticket=ticket, content=serializer.data["content"], ** extra)
            print(fed)
            # fed2 = Feedback.objects.get(
            #     ticket=ticket, owner=request.user, id=self.id)
            # print(fed2)
            return Response(FeedbackSerializers(fed).data, status=201)
        else:
            return Response({"errors": serializer.errors}, status=400)


class FeedBackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializers
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Feedback.objects.all()
    lookup_field = 'id'


class FeedBackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializers
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Feedback.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Feedback.objects.filter(owner=self.request.user)
        return queryset


class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        all_images = FeedBackImage.objects.filter(feedback=id)
        serializer = ImageSerializer(all_images, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        # feedback = request.data['feedback']
        feedback = get_object_or_404(Feedback, id=id)
        # print(feedback)

        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []

        for img_name in images:
            modified_data = modify_input_for_multiple_files(feedback.id,
                                                            img_name)

            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class ProDistList(APIView):
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    pagination_class = SmallPagination

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        client = User.objects.get(email=ticket.owner)
        client_lat_long = (float(client.latitude), float(client.longitude))
        pro = User.objects.filter(is_pro=True)
        pro_dict_temp = {}
        pro_list = []
        for i in pro:
            pro_lat_long = (float(i.latitude), float(i.longitude))
            dist = geodesic(client_lat_long, pro_lat_long).km
            pro_dict_temp["id"] = i.id
            pro_dict_temp["distance"] = round(dist, 3)
            pro_dict_temp["company_name"] = i.company_name
            pro_dict_temp["phone"] = i.phone_number
            pro_dict = pro_dict_temp.copy()
            pro_list.append(pro_dict)
        pro_list_sorted = sorted(pro_list, key=lambda i: i["distance"])
        return Response(pro_list_sorted)
