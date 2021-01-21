from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView, LogoutAPIView, RequestPasswordResetEmail, 
                    PasswordTokenCheckAPI, SetNewPasswordAPIView, ProRegisterView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-pro/', ProRegisterView.as_view(), name='register-pro'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete')
]
