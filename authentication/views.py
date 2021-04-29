from django.db.models.expressions import F
from .serializers import (RegisterSerializer, EmailVerificationSerializer,
                          LoginSerializer, LogoutSerializer, ResetPasswordEmailRequestSerializer,
                          SetNewPasswordSerializer, ProRegisterSerializer, UserDetailSerializer, MyTokenObtainPairSerializer, ServiceTypeSerializers)
from .models import ServiceType, User
from ticket.models import Ticket, Feedback
from .renderers import UserJSONRenderer
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, status, views, permissions, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,  smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.views import TokenObtainPairView
from .permission import IsConnectorUser, IsCurrentUser
from bbank.pagination import SmallPagination, LargePagination
from bbank.utils import EmailUtil
from django.db.models import Q, Count, Subquery, OuterRef
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as djfilters
from .coordinate import find_lat_long
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView


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
        user.zip_address = request.data['zip_address']
        user.latitude = find_lat_long(user_data['zip_address']
                                      )["geocodePoints"][0]["coordinates"][0]
        user.longitude = find_lat_long(user_data['zip_address']
                                       )["geocodePoints"][0]["coordinates"][1]
        user.save()
        # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hi '+user.username + \
        #     ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}

        try:
            EmailUtil.send_email(request, user)
        except:
            return Response({'detail': 'Couldn not send email'}, status=status.HTTP_400_BAD_REQUEST)

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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_connector = True
        user.zip_address = request.data['zip_address']
        user.latitude = find_lat_long(user_data['zip_address']
                                      )["geocodePoints"][0]["coordinates"][0]
        user.longitude = find_lat_long(user_data['zip_address']
                                       )["geocodePoints"][0]["coordinates"][1]
        user.save()
        try:
            EmailUtil.send_email(request, user)
        except:
            return Response({'detail': 'Couldn not send email'}, status=status.HTTP_400_BAD_REQUEST)
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
            user.zip_address = request.data['zip_address']
            user.latitude = find_lat_long(user_data['zip_address']
                                          )["geocodePoints"][0]["coordinates"][0]
            user.longitude = find_lat_long(user_data['zip_address']
                                           )["geocodePoints"][0]["coordinates"][1]
            user.save()
            try:
                EmailUtil.send_email(request, user)
            except:
                return Response({'detail': 'Couldn not send email'}, status=status.HTTP_400_BAD_REQUEST)

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

            user.reserved_capacity = request.data['reserved_capacity']
            user.latitude = find_lat_long(user_data['zip_address']
                                          )["geocodePoints"][0]["coordinates"][0]
            user.longitude = find_lat_long(user_data['zip_address']
                                           )["geocodePoints"][0]["coordinates"][1]

            # user.service_type = request.data['service_type']
            # print(request.data['service_type'])
            # for service in request.data['service_type']:
            #     obj = ServiceType.objects.get(id=service)
            #     user.service_type.add(obj)
            user.save()
            try:
                EmailUtil.send_email(request, user)
            except:
                return Response({'detail': 'Couldn not send email'}, status=status.HTTP_400_BAD_REQUEST)
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
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)
            FRONTEND_URL = config('FRONTEND_URL')

            verify_link = FRONTEND_URL + 'login?' + \
                "token=" + str(token)+"&uidb64=" + \
                str(uidb64) + "&resetPassword=true"

            subject, from_email, to = 'Reset Your Password', config(
                'EMAIL_HOST_USER'), user.email
            current_site = get_current_site(request).domain
            html_content = render_to_string('reset_password.html', {
                                            'verify_link': verify_link, 'base_url': FRONTEND_URL, 'backend_url': current_site, 'user': user})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# class PassordResetRequestView(GenericAPIView):
#     """
#     allow users to request for a password reset token provided the email is valid
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = PasswordResetResquestSerializer

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         user = User.objects.filter(email=email).first()
#         if user:
#             token = user.generated_jwt_token()
#             user.send_password_reset_link(request, token)
#             return Response(
#                 {'message': 'password reset link has been sent to your email'},
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response({'error': 'the email does not match any account'},
#                             status=status.HTTP_400_BAD_REQUEST
#                             )


# class PasswordResetView(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = PasswordResetSerializser

#     def put(self, request, *args, **kwargs):
#         token = kwargs.pop('token')
#         try:
#             user = jwt.decode(token, SECRET_KEY)
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'token expired'})
#         user_detail = User.objects.get(pk=user['id'])
#         data = request.data.get('user', {})
#         if data['password'] == data['confirmpassword']:
#             serializer = self.serializer_class(user_detail, data=data)
#             serializer.is_valid(raise_exception=True)
#             user_detail.set_password(data['password'])
#             user_detail.save()
#             return Response(
#                 {"message": "your password has been reset successfully"},
#                 status=status.HTTP_200_OK
#             )

#         else:
#             return Response(
#                 {"error": "password and confirm password fields do not match"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


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
    # renderer_classes = (UserJSONRenderer,)

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.kwargs["username"]
        queryset = queryset.filter(username=username)
        return queryset


class UserRemoveView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsCurrentUser)
    #serializer_class = serializer_class = UserDetailSerializer

    def post(self, request, **extra):
        #serializer = self.serializer_class(data=request.data)
        current_user = User.objects.get(username=request.user.username)
        current_user.email = f"xxxx{current_user.id}@mail.com"
        current_user.username = f"xxxx{current_user.id}"
        current_user.first_name = "xxxx"
        current_user.last_name = "xxxx"
        current_user.address = "xxxx"
        current_user.zip_address = "xxxx"
        current_user.company_name = "xxxx"
        current_user.phone_number = "xxxx"
        current_user.phone_number2 = "xxxx"
        current_user.about_me = "xxxx"
        current_user.profile_image = None
        current_user.is_active = False
        current_user.is_verified = False
        current_user.is_staff = False
        current_user.save()
        tickets = Ticket.objects.filter(owner=request.user)
        for ticket in tickets:
            ticket.email = f"xxxx{current_user.id}@mail.com"
            ticket.first_name = "xxxx"
            ticket.last_name = "xxxx"
            ticket.phone_number = "xxxx"
            ticket.phone_number2 = "xxxx"
            ticket.about_me = "xxxx"
            ticket.save()

        data = {
            "messages": "Remove Successfuly"}

        return Response(data, status=status.HTTP_200_OK)


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


class ServiceTypeView(generics.ListAPIView):
    serializer_class = ServiceTypeSerializers
    permission_classes = (AllowAny,)
    queryset = ServiceType.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConnectorUser,)
    pagination_class = SmallPagination
    # renderer_classes = (UserJSONRenderer,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter, djfilters.DjangoFilterBackend,)
    search_fields = ("username", 'email', 'first_name',
                     'last_name', 'company_name', 'address', 'phone_number', 'phone_number2', 'zip_address')
    ordering_fields = ['is_gray', 'is_client',
                       'is_pro', 'is_sponsor', 'is_connector']
    filterset_fields = ['is_gray', 'is_client',
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
                Q(last_name__icontains=keyword) |
                Q(address__icontains=keyword) |
                Q(phone_number__icontains=keyword) |
                Q(phone_number2__icontains=keyword) |
                Q(zip_address__icontains=keyword)
            ).distinct()

            return queryset
        else:
            return queryset
