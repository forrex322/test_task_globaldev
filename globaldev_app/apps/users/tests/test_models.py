import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import User, Profile
from users.tests.factories import UserFactory, ProfileFactory

pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user(self):
        proto_user = UserFactory.build()
        user = User.objects.create_user(
            email=proto_user.email,
            password=proto_user._password,
            first_name=proto_user.first_name,
            last_name=proto_user.last_name,
            username=proto_user.username,
        )

        assert User.objects.filter(email=proto_user.email).exists()
        assert user.email == proto_user.email
        assert user.first_name == proto_user.first_name
        assert user.last_name == proto_user.last_name
        assert user.username == proto_user.username
        assert user.check_password(proto_user._password)
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active

        with pytest.raises(ValueError, match="The given email must be set"):
            User.objects.create_user(
                email="",
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                username=proto_user.username,
            )

        with pytest.raises(ValueError, match="The given username must be set"):
            User.objects.create_user(
                email=proto_user.email,
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                username="",
            )

    def test_create_superuser(self):
        proto_user = UserFactory.build()
        user = User.objects.create_superuser(
            email=proto_user.email,
            password=proto_user._password,
            first_name=proto_user.first_name,
            last_name=proto_user.last_name,
            username=proto_user.username,
        )

        assert User.objects.filter(email=proto_user.email).exists()
        assert user.email == proto_user.email
        assert user.first_name == proto_user.first_name
        assert user.last_name == proto_user.last_name
        assert user.username == proto_user.username
        assert user.check_password(proto_user._password)
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

        with pytest.raises(ValueError, match="The given email must be set"):
            User.objects.create_superuser(
                email="",
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                username=proto_user.username,
            )

        with pytest.raises(ValueError, match="The given username must be set"):
            User.objects.create_superuser(
                email=proto_user.email,
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                username="",
            )

        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(
                email=proto_user.email,
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                is_staff=False,
                username=proto_user.username,
            )

        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(
                email=proto_user.email,
                password=proto_user._password,
                first_name=proto_user.first_name,
                last_name=proto_user.last_name,
                is_superuser=False,
                username=proto_user.username,
            )


class TestUser:
    def test_get_full_name(self, user):
        assert user.get_full_name() == f"{user.first_name} {user.last_name}".strip()

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name

    @pytest.mark.skip(reason="Public profiles are not ready yet")
    def test_user_get_absolute_url(self, user):
        assert user.get_absolute_url() == "/api/v1/auth/user/"


class TestProfile:
    def test_name_methods(self):
        profile = ProfileFactory()
        user = profile.user

        assert profile.first_name == user.first_name
        assert profile.last_name == user.last_name
        assert profile.full_name == user.get_full_name()

    def test_birth_date_validation(self):
        profile = ProfileFactory()

        assert profile.full_clean() is None

        profile.birth_date = timezone.now().date() + timezone.timedelta(days=2)
        with pytest.raises(ValidationError):
            profile.full_clean()

        profile.birth_date = timezone.datetime(199, 1, 1).date()
        with pytest.raises(ValidationError):
            profile.full_clean()
