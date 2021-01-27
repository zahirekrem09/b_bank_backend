from django.urls import path
from .views import (TicketsView, TicketsDetailView,)

urlpatterns = [
    path('tickets/', TicketsView.as_view(), name='tickets-list'),
    path('tickets/<int:id>', TicketsDetailView.as_view(), name='tickets-detail'),

]
