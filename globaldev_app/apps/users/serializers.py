from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Sum
from django.utils.translation import gettext as _

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_auth.models import TokenModel
from rest_auth.serializers import (
    TokenSerializer as BaseTokenSerializer,
)

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from booktimetracker.models import ReadingSession
from users.models import User, Profile

UserModel = get_user_model()


class RegisterSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for registration a new user.
    """

    email = serializers.EmailField(required=True, help_text=_("Email address"))
    password1 = serializers.CharField(write_only=True, help_text=_("Password"))
    password2 = serializers.CharField(
        write_only=True, help_text=_("Password Confirmation")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = {}

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address.")
            )
        return email

    @staticmethod
    def validate_password1(password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return attrs

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):  # pylint: disable=arguments-differ
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserShortSerializer(serializers.ModelSerializer):
    """
    Serializer that returns short information about user.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )
        read_only_fields = fields


class TokenSerializer(BaseTokenSerializer):
    """
    Serializer that returns token for user authentication.
    """

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ("key", "user")
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for work with user's profile.
    """

    username = serializers.CharField(
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    first_name = serializers.CharField(max_length=30, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    total_reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        user_fields = ("username", "first_name", "last_name")
        fields = (
            "description",
            "birth_date",
            "total_reading_time",
            "last_7_days_statistic",
            "last_30_days_statistic",
        ) + user_fields

    def update(self, instance, validated_data):
        validated_data = self._update_user(instance, validated_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields["username"] = serializers.CharField(source="user.username")
        self.fields["first_name"] = serializers.CharField(source="user.first_name")
        self.fields["last_name"] = serializers.CharField(source="user.last_name")
        return super().to_representation(instance)

    def _update_user(self, instance, validated_data):
        user = instance.user

        user_data = {}
        profile_data = {}
        for field, value in validated_data.items():
            if field in self.Meta.user_fields:
                user_data[field] = value
            else:
                profile_data[field] = value

        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()

        return profile_data

    @staticmethod
    def get_total_reading_time(obj):
        data = ReadingSession.objects.filter(user=obj.user).aggregate(
            total_reading_time=Sum("duration_of_session")
        )
        return str(data["total_reading_time"])
