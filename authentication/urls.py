from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView, LogoutAPIView, RequestPasswordResetEmail,
                    PasswordTokenCheckAPI, SetNewPasswordAPIView, ProRegisterView, ConnectorRegisterView, UserDetail, SponsorRegisterView, MyObtainTokenPairView, UserListView, ConnectorUserDetail)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-pro/', ProRegisterView.as_view(), name='register-pro'),
    path('register-sponsor/', SponsorRegisterView.as_view(),
         name='register-sponsor'),
    path('register-connector/', ConnectorRegisterView.as_view(),
         name='register-connector'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user-detail/<str:username>', UserDetail.as_view(), name='user-detail'),
    path('connector-user-detail/<str:username>',
         ConnectorUserDetail.as_view(), name='connector-user-detail'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(),
         name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-list/', UserListView.as_view(), name='user-list'),
]
