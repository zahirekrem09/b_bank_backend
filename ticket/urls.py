from django.urls import path
from .views import (CreateTicketsView, ClientTicketsDetailView,
                    ConnectorTicketsDetailView, TicketListView)

urlpatterns = [
    path('create/', CreateTicketsView.as_view(), name='ticket-create'),
    path('ticket-list/', TicketListView.as_view(), name='ticket-list'),
    path('client-tickets/<int:id>', ClientTicketsDetailView.as_view(),
         name='client-tickets-detail'),
    path('connector-tickets/<int:id>', ConnectorTicketsDetailView.as_view(),
         name='connector-tickets-detail'),

]
