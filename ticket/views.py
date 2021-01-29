from django.shortcuts import render
from .serializers import (
    TicketSerializer, TicketClientDetailSerializer, TicketConnectorDetailSerializer)
from .models import Ticket
from django.shortcuts import render
from .permission import IsOwnerOrReadOnly
from rest_framework.views import APIView
from authentication.models import User
from authentication.permission import IsConnectorUser
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response


class CreateTicketsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, **extra):
        owner = User.objects.get(username=request.user.username)
        print(owner)
        Ticket.objects.create(owner=owner, **extra)

        data = {
            "messages": "Create Ticket Successfuly"
        }

        return Response(data, status=status.HTTP_201_CREATED)


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ticket.objects.filter(owner=self.request.user)
        return queryset


class ClientTicketsDetailView(generics.UpdateAPIView):
    serializer_class = TicketClientDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ticket.objects.filter(owner=self.request.user)
        return queryset


class ConnectorTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketConnectorDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser)
    # TODO: connector permission yazılıcak
    queryset = Ticket.objects.all()
    lookup_field = 'id'
