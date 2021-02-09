from .serializers import (RegisterSerializer, EmailVerificationSerializer,
                          LoginSerializer, LogoutSerializer, ResetPasswordEmailRequestSerializer,
                          SetNewPasswordSerializer, ProRegisterSerializer, UserDetailSerializer, MyTokenObtainPairSerializer)
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions
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


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


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
        FRONTEND_URL = "http://localhost:3000"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + '/email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(user_data, status=status.HTTP_201_CREATED)


class ConnectorRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_connector = True
        user.save()    
        FRONTEND_URL = "http://localhost:3000"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + '/email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(user_data, status=status.HTTP_201_CREATED)


class SponsorRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_sponsor = True
        user.save()
        FRONTEND_URL = "http://localhost:3000"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + '/email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response(user_data, status=status.HTTP_201_CREATED)


class ProRegisterView(generics.GenericAPIView):
    serializer_class = ProRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        FRONTEND_URL = "http://localhost:3000"

        token = RefreshToken.for_user(user).access_token
        verify_link = FRONTEND_URL + '/email-verify/' + str(token)
        subject, from_email, to = 'Verify Your Email', 'bbankdummymail@gmail.com', user.email
        current_site = get_current_site(request).domain
        html_content = render_to_string('verify_email.html', {
                                        'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Util.send_email(data)
        return Response(self.serializer_class(User.objects.get(email=user_data['email'])).data, status=status.HTTP_201_CREATED)


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


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsCurrentUser)
    lookup_field = 'username'
    # TODO: Custom permission

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.kwargs["username"]
        queryset = queryset.filter(username=username)
        return queryset
