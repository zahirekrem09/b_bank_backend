from .serializers import (RegisterSerializer, EmailVerificationSerializer,
                          LoginSerializer, LogoutSerializer, ResetPasswordEmailRequestSerializer,
                          SetNewPasswordSerializer, ProRegisterSerializer, UserDetailSerializer, MyTokenObtainPairSerializer)
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import jwt
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .permission import IsCurrentUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.views import TokenObtainPairView
from .permission import IsConnectorUser
from bbank.pagination import SmallPagination, LargePagination
from django.db.models import Q, Count, Subquery, OuterRef


"""
@Path: /auth/token => path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair')
@Method: POST
@Permisson: Public
@Decs: Altarnatif Login
"""


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


"""
@Path: /auth/register => path('register/', RegisterView.as_view(), name='register'),
@Method: POST
@Permisson: Public
@Decs: Client Register
"""


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_client = True
        user.save()
        # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hi '+user.username + \
        #     ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}

        # Util.send_email(data)
        # print(f"user in db {user}")
        FRONTEND_URL = "https://beauty-bank-frontend.herokuapp.com/"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + 'email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(user_data, status=status.HTTP_201_CREATED)


"""
@Path: /auth/'register-connector => path('register-connector/', ConnectorRegisterView.as_view(),name='register-connector'),
@Method: POST
@Permisson: Public
@Decs: Connector Register
"""


class ConnectorRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_connector = True
        user.save()
        print(user)
        FRONTEND_URL = "https://beauty-bank-frontend.herokuapp.com/"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + 'email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(user_data, status=status.HTTP_201_CREATED)


"""
@Path: /auth/register => path('register-sponsor/', SponsorRegisterView.as_view(),name='register-sponsor'),
@Method: POST
@Permisson: Public
@Decs: Sponsor Register
"""


class SponsorRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.is_sponsor = True
            user.save()
            FRONTEND_URL = "https://beauty-bank-frontend.herokuapp.com/"

            token = RefreshToken.for_user(user).access_token
            verify_link = FRONTEND_URL + 'email-verify/' + str(token)
            subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
            current_site = get_current_site(request).domain
            html_content = render_to_string('verify_email.html', {
                                            'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
@Path: /auth/register-pro => path('register-pro/', ProRegisterView.as_view(), name='register-pro'),
@Method: POST
@Permisson: Public
@Decs: Pro Register
"""


class ProRegisterView(generics.GenericAPIView):
    serializer_class = ProRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.is_pro = True
            user.company_name = request.data['company_name']
            user.for_gender = request.data['for_gender']
            user.zip_address = request.data['zip_address']
            user.about_me = request.data['about_me']
            user.service_type = request.data['service_type']
            user.reserved_capacity = request.data['reserved_capacity']
            user.save()
            FRONTEND_URL = "https://beauty-bank-frontend.herokuapp.com/"

            token = RefreshToken.for_user(user).access_token
            verify_link = FRONTEND_URL + 'email-verify/' + str(token)
            subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
            current_site = get_current_site(request).domain
            html_content = render_to_string('verify_email.html', {
                                            'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Util.send_email(data)
            return Response(self.serializer_class(User.objects.get(email=user_data['email'])).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
@Path: /auth/email-verify => path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
@Method: POST
@Permisson: Public
@Decs: Email Activate
"""


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        token = request.data['token']
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


"""
@Path: /auth/login => path('login/', LoginAPIView.as_view(), name='login'),
@Method: POST
@Permisson: Public
@Decs: Login
"""


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
@Path: /auth/logout => path('logout/', LogoutAPIView.as_view(), name='logout'),
@Method: POST
@Permisson: Private
@Decs: Login
"""


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

# method_2


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""
@Path: /auth/request-reset-email => path('request-reset-email', RequestPasswordResetEmail.as_view(),
                            name='request-reset-email'),
@Method: POST
@Permisson: Public
@Decs: Reset Pasword Send Email 
"""


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hello '+user.username + \
                ' Use the link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}

            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


"""
@Path: /auth/password-reset/<uidb64>/<token>/ => path('password-reset/<uidb64>/<token>/',
                                  PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
@Method: GET
@Permisson: Public
@Decs: Password Reset Confirm 
"""


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token})

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


"""
@Path: /auth/password-reset-complete => path('password-reset-complete', SetNewPasswordAPIView.as_view(),
                                                  name='password-reset-complete'),
@Method: PATCH
@Permisson: Public
@Decs: Set New Password  
"""


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


"""
@Path: /auth/user-detail/<str:username> => path('user-detail/<str:username>', UserDetail.as_view(), name='user-detail'),
@Method: GET
@Permisson: Private
@Decs: User Detail   
"""


class UserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsCurrentUser)
    lookup_field = 'username'

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.kwargs["username"]
        queryset = queryset.filter(username=username)
        return queryset


class ConnectorUserDetail(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser)
    lookup_field = 'username'

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.kwargs["username"]
        queryset = queryset.filter(username=username)
        return queryset


"""
@Path: /auth/user-list => path('user-list/', UserListView.as_view(), name='user-list'),
@Method: GET
@Permisson: Private just Connector 
@Decs: User List   
"""


class UserListView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    pagination_class = SmallPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ("username", 'email', 'first_name',
                     'last_name', 'company_name')
    ordering_fields = ['is_gray', 'is_client',
                       'is_pro', 'is_sponsor', 'is_connector']
    queryset = User.objects.all().order_by('-created_at')
    lookup_field = 'id'

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        if self.request.method.lower() != "get":
            return queryset
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword) |
                Q(email__icontains=keyword) |
                Q(first_name__icontains=keyword) |
                Q(last_name__icontains=keyword)
            ).distinct()

            return queryset
        else:
            return queryset
