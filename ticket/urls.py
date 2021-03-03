from django.urls import path
from .views import (CreateTicketsView, ClientTicketsDetailView,
                    ConnectorTicketsDetailView, TicketListView, ImageView, FeedBackCreateView, FeedBackListView, ConfirmTicketsView, ClientTicketsListView)

urlpatterns = [
    path('create/', CreateTicketsView.as_view(), name='ticket-create'),
    path('client-ticket-list/', ClientTicketsListView.as_view(),
         name='client-ticket-list'),
    path('ticket-list/', TicketListView.as_view(), name='ticket-list'),
    path('client-tickets/<int:id>', ClientTicketsDetailView.as_view(),
         name='client-tickets-detail'),
    path('connector-tickets/<int:id>', ConnectorTicketsDetailView.as_view(),
         name='connector-tickets-detail'),
    path('feedback-imageupload/<int:id>', ImageView.as_view(),
         name="feedback-imageupload"),
    path('feedback/<int:id>', FeedBackCreateView.as_view(),
         name="feedback"),
    path('feedback-list/', FeedBackListView.as_view(),
         name="feedback-list"),
    path('confirm/<int:id>', ConfirmTicketsView.as_view(),
         name='ticket-confirm'),
]
