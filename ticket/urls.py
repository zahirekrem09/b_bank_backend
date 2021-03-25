from django.urls import path
from .views import (CreateTicketsView, ClientTicketsDetailView,
                    ConnectorTicketsDetailView, TicketListView, ImageView, FeedBackCreateView, FeedBackListView, ConfirmTicketsView, ClientTicketsListView, TicketTermsApprovedView, FeedBackDetailView, ProDistList)

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

    path('feedback-create/<int:id>/', FeedBackCreateView.as_view(),
         name="feedback"),
    path('feedback-list/', FeedBackListView.as_view(),
         name="feedback-list"),
    path('feedback/<int:id>', FeedBackDetailView.as_view(),
         name="feedback-detail"),
    path('confirm/<int:id>', ConfirmTicketsView.as_view(),
         name='ticket-confirm'),
    path('terms-approved/', TicketTermsApprovedView.as_view(),
         name='tickets-terms_approved'),
    path('dist-list/<int:id>', ProDistList.as_view(),
         name='pro-dist-list'),
]
