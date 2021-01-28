from django.shortcuts import render
from .serializers import (TicketSerializer, TicketClientDetailSerializer, TicketConnectorDetailSerializer)
from .models import Ticket
from django.shortcuts import render
from .permission import IsOwnerOrReadOnly

from rest_framework import generics, status, views, permissions


class TicketsView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Ticket.objects.all()


class ClientTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketClientDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Ticket.objects.all()
    lookup_field = 'id'

class ConnectorTicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketConnectorDetailSerializer
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Ticket.objects.all()
    lookup_field = 'id'
