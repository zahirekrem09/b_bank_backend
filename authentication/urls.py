from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, LogoutAPIView, ProRegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-pro/', ProRegisterView.as_view(), name='register-pro'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify')
]
