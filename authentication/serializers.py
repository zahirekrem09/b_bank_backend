from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User, UserManager
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name',
                  'last_name', 'phone_number', 'gdpr_consent']

    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     username = attrs.get('username', '')

    #     if not username.isalnum():
    #         raise serializers.ValidationError(
    #             self.default_error_messages)
    #     return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name',
                  'last_name', 'zip_address', 'phone_number', 'about_me', 'company_name', 'for_gender', 'reserved_capacity', 'service_type', 'gdpr_consent']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def get_role(self, obj):
        user = User.objects.get(email=obj['email'])

        if user.is_pro:
            return "Pro"

        elif user.is_client:
            return "Client"

        elif user.is_sponsor:
            return "Sponsor"

        elif user.is_connector:
            return "Connector"

        else:
            return "Admin"

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'role']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return(user)

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

        return super().validate(attrs)


class UserDetailSerializer(serializers.ModelSerializer):
    service_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ("password", )
        # fields = '__all__'
        lookup_field = "username"

    def get_service_type(self, obj):
        return obj.get_service_type_display()


class UserTicketOwnerSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    transportation_type = serializers.SerializerMethodField()
    preferred_lang = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name",
                  "last_name", "gender", "zip_address", "phone_number", "phone_number2", "about_me", "transportation_type", "preferred_lang", "gdpr_consent", "is_gray", "company_name", "address")

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_transportation_type(self, obj):
        return obj.get_transportation_type_display()

    def get_preferred_lang(self, obj):
        return obj.get_preferred_lang_display()


class UserTicketProSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    company_name = serializers.CharField()
    phone_number = serializers.CharField()
    phone_number2 = serializers.CharField()
