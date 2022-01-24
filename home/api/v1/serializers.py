from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from home.models import *
from home.constants import APP_CHOICES_LIST, FRAMEWORK_CHOICES_LIST


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm

class AppSerializer(serializers.ModelSerializer):
    # App Model Serializer for CRUD operations
    type = serializers.CharField(max_length=6)
    framework = serializers.CharField(max_length=12)
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'type', 'framework', 'domain_name', 'screenshot', 'subscription', 'user', 'created_at', 'updated_at']

    # Overriding type validate method for custom error message
    def validate_type(self, type):
        if type not in APP_CHOICES_LIST:
            raise serializers.ValidationError(_(f'{type} is not a valid app type. Valid values are {APP_CHOICES_LIST}'))
        return type

    # Overriding framework validate method for custom error message
    def validate_framework(self, framework):
        if framework not in FRAMEWORK_CHOICES_LIST:
            raise serializers.ValidationError(_(f'{framework} is not a valid framework type. Valid values are  {FRAMEWORK_CHOICES_LIST}'))
        return framework

    # Overriding create method for fields values overriding
    def create(self, validated_data):
        app = App(
            name=validated_data.get('name'),
            type=validated_data.get('type'),
            description=validated_data.get('description'),
            framework=validated_data.get('framework'),
            domain_name=validated_data.get('domain_name'),
            screenshot=f"{validated_data.get('name').replace(' ', '_').lower()}_screenshot.png",
            user = validated_data.get('user')
        )
        app.save()
        return app

    # Overriding update method for selective fields update
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name')
        instance.type=validated_data.get('type')
        instance.framework=validated_data.get('framework')
        if 'description' in validated_data:
            instance.description=validated_data.get('description')
        if 'domain_name' in validated_data:
            instance.domain_name=validated_data.get('domain_name')
        instance.save()
        return instance

class PlanSerializer(serializers.ModelSerializer):
    # Plan Model Serializer for CRUD operations
    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    # Subscription Model Serializer for CRUD operations
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'app', 'active', 'created_at', 'updated_at']