from django.urls import path
from .views import (TicketsView, ClientTicketsDetailView, ConnectorTicketsDetailView)

urlpatterns = [
    path('tickets/', TicketsView.as_view(), name='tickets-list'),
    path('client-tickets/<int:id>', ClientTicketsDetailView.as_view(), name='client-tickets-detail'),
    path('connector-tickets/<int:id>', ConnectorTicketsDetailView.as_view(), name='connector-tickets-detail'),

]
