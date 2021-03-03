from django.shortcuts import render, get_object_or_404
from .serializers import (
    TicketSerializer, TicketClientDetailSerializer, TicketConnectorDetailSerializer, ImageSerializer, FeedbackCreateSerializers, FeedbackSerializers, TicketClientCreateSerializer)
from .models import FeedBackImage, Feedback, Ticket
from .helpers import modify_input_for_multiple_files
from django.shortcuts import render
from .permission import IsOwnerOrReadOnly
from rest_framework.views import APIView
from authentication.models import User
from authentication.permission import IsConnectorUser
from rest_framework import generics, status, views, permissions, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q, Count, Subquery, OuterRef


class CreateTicketsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TicketClientCreateSerializer

    def post(self, request, **extra):
        serializer = self.serializer_class(data=request.data)
        owner = User.objects.get(username=request.user.username)
        Ticket.objects.create(owner=owner, email=owner.email,
                              first_name=owner.first_name, last_name=owner.last_name, phone_number=owner.phone_number, about_me=owner.about_me, service_type=request.data['service_type'], ** extra)

        data = {
            "messages": "Create Ticket Successfuly"
        }

        return Response(data, status=status.HTTP_201_CREATED)


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
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    queryset = Ticket.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ("owner__username", 'email', 'first_name', 'last_name',)
    lookup_field = 'id'

    # def get_queryset(self):
    #     queryset = Ticket.objects.all()
    #     if self.request.method.lower() != "get":
    #         return queryset
    #     keyword = self.request.GET.get('keyword')
    #     if keyword:
    #         queryset = queryset.filter(
    #             Q(owner__username__icontains=keyword) |
    #             Q(email__icontains=keyword) |
    #             Q(first_name__icontains=keyword) |
    #             Q(last_name__icontains=keyword)

    #         ).distinct()

    #         return queryset
    #     else:
    #         return queryset


class ClientTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketClientDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
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


class FeedBackCreateView(APIView):
    # serializer_class = FeedbackSerializers
    permission_classes = (permissions.IsAuthenticated,)
    # queryset = Feedback.objects.all()
    # lookup_field = 'id'
    serializer_class = FeedbackCreateSerializers

    def post(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        # print(ticket.id)
        serializer = FeedbackCreateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, ticket=ticket)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


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
        print(feedback)

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
