import pytest

from django.urls import reverse
from rest_framework import status

from users.models import User
from users.tests.factories import UserFactory, ProfileFactory, USER_PASSWORD

pytestmark = pytest.mark.django_db


class TestRegistrationAPIViewSet:
    registration_url = reverse("api:users:auth:register")

    def test_registration(self, api_client):
        proto_user = UserFactory.build()

        signup_payload = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert User.objects.filter(email=proto_user.email).exists()

    def test_invalid_registration(self, api_client):
        proto_user = UserFactory.build()

        signup_payload = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": "another_password",
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            "The two password fields didn't match." in response.data["non_field_errors"]
        )

        user = UserFactory()

        signup_payload = {
            "email": user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            "A user is already registered with this e-mail address."
            in response.data["email"]
        )


class TestLoginView:
    login_url = reverse("api:users:auth:login")

    def test_login_via_email(self, api_client):
        user = UserFactory()
        password = USER_PASSWORD

        login_payload = {"email": user.email, "password": password}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.wsgi_request.user.is_authenticated

        data = response.data
        assert "key" in data.keys()
        assert data["key"]
        assert "user" in data.keys()
        assert data["user"]["id"] == user.id
        assert data["user"]["email"] == user.email

    def test_login_with_invalid_credentials(self, api_client):
        expected_text_message = "Unable to log in with provided credentials."

        # 1. Test with bad password
        user = UserFactory()

        good_password = "String123"
        bad_password = "321"
        user.set_password(good_password)
        user.save()

        login_payload = {"email": user.email, "password": bad_password}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not response.wsgi_request.user.is_authenticated
        assert response.data["non_field_errors"][0] == expected_text_message

        # 2. Test with bad email
        good_email = "test@test.com"
        bad_email = "123tesxcvv33"
        user.email = good_email
        user.save()

        login_payload = {"email": bad_email, "password": good_password}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not response.wsgi_request.user.is_authenticated
        assert response.data["email"][0] == "Enter a valid email address."


class TestLogoutView:
    logout_url = reverse("api:users:auth:logout")

    def test_happy_path(self, api_client, user):
        api_client.force_authenticate(user)

        response = api_client.post(self.logout_url)

        assert response.status_code == status.HTTP_200_OK
        assert not response.wsgi_request.user.is_authenticated


class TestProfileAPIViewSet:
    profile_detail_url = reverse("api:users:profiles:my-detail")

    def test_authorization(self, api_client):
        response = api_client.get(self.profile_detail_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_allowed_methods(self, api_client, user):
        api_client.force_authenticate(user)

        response = api_client.delete(self.profile_detail_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_client.post(self.profile_detail_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_client.get(self.profile_detail_url)
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_client.patch(self.profile_detail_url)
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_client.put(self.profile_detail_url)
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_retrieve(self, api_client, user):
        api_client.force_authenticate(user)

        response = api_client.get(self.profile_detail_url)
        assert response.status_code == status.HTTP_200_OK

        data = response.data

        assert data["username"] == user.username
        assert data["last_name"] == user.last_name
        assert data["first_name"] == user.first_name
        assert data["description"] == user.profile.description
        assert data["last_7_days_statistic"] == user.profile.last_7_days_statistic
        assert data["last_7_days_statistic"] == user.profile.last_30_days_statistic

    def test_partial_update(self, api_client, user):
        api_client.force_authenticate(user)

        new_profile_data = ProfileFactory.build()
        new_user_data = UserFactory.build()

        data = {
            "description": new_profile_data.description,
            "last_name": new_user_data.last_name,
        }
        old_username = user.username
        old_first_name = user.first_name

        response = api_client.patch(self.profile_detail_url, data)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.last_name == data["last_name"]
        assert user.profile.description == data["description"]
        # Ensure that other fields are unaffected
        assert user.first_name == old_first_name
        assert user.username == old_username

    def test_update(self, api_client, user):
        api_client.force_authenticate(user)

        new_profile_data = ProfileFactory.build()
        new_user_data = UserFactory.build()

        data = {
            "birth_date": new_profile_data.birth_date,
            "description": new_profile_data.description,
            "first_name": new_user_data.first_name,
            "last_name": new_user_data.last_name,
            "username": new_user_data.username,
        }

        response = api_client.put(self.profile_detail_url, data)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.profile.description == data["description"]
        assert user.profile.birth_date == data["birth_date"]
        assert user.last_name == data["last_name"]
        assert user.first_name == data["first_name"]
        assert user.username == data["username"]


class TestPasswordChangeView:
    password_change_url = reverse("api:users:auth:password-change")

    def test_view_permission(self, api_client):
        response = api_client.post(self.password_change_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_password_change(self, api_client):
        password = USER_PASSWORD
        new_password = "new_P@ssword11"
        user = UserFactory(password=password)
        api_client.force_authenticate(user)

        data = {
            "old_password": "random password",
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = api_client.post(self.password_change_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data["old_password"] = password

        response = api_client.post(self.password_change_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        assert user.check_password(new_password)
