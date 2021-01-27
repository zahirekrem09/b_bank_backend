from django.shortcuts import render
from .serializers import (TicketSerializer, TicketClientDetailSerializer)
from .models import Ticket
from django.shortcuts import render


from rest_framework import generics, status, views, permissions


class TicketsView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Ticket.objects.all()


class TicketsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketClientDetailSerializer
    queryset = Ticket.objects.all()
    lookup_field = 'id'
