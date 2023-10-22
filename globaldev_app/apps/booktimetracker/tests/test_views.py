import pytest

from django.urls import reverse
from rest_framework import status

from booktimetracker.models import ReadingSession
from booktimetracker.tests.factories import BookFactory, ReadingSessionFactory

pytestmark = pytest.mark.django_db


class TestBookAPIViewSet:
    list_url = reverse("api:booktimetracker:books-list")

    def test_list_of_books(self, api_client, user):
        api_client.force_authenticate(user)

        number_of_books = 5
        books = BookFactory.create_batch(number_of_books)

        response = api_client.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == number_of_books

    def test_retrieve_book(self, api_client, user):
        api_client.force_authenticate(user)

        book = BookFactory()
        reading_session = ReadingSessionFactory(book=book)

        url = reverse("api:booktimetracker:books-detail", kwargs={"pk": book.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == book.id
        assert response.data["name"] == book.name
        assert response.data["author"] == book.author
        assert response.data["date_of_publication"] == book.date_of_publication
        assert response.data["short_description"] == book.short_description
        assert response.data["full_description"] == book.full_description
        assert (
            response.data["date_of_last_reading"]
            == reading_session.start_reading_session
        )


class TestReadingSessionViewSet:
    create_url = reverse("api:booktimetracker:reading_sessions-list")

    @pytest.mark.freeze_time("2023-10-22T00:00:00Z")
    def test_start_reading_session(self, user, api_client):
        api_client.force_authenticate(user)
        book = BookFactory()

        proto_reading_session = ReadingSessionFactory.build()
        payload_data = {"book": book.id}

        response = api_client.post(self.create_url, data=payload_data)

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert response.data["book"]["id"] == book.id
        assert response.data["user"]["id"] == user.id
        assert response.data["start_reading_session"] == "2023-10-22T00:00:00Z"

    def test_start_reading_session_bad(self, user, api_client):
        api_client.force_authenticate(user)
        book = BookFactory()
        error_message = (
            "You can't start a new reading session, because old one isn't closed."
        )

        proto_reading_session = ReadingSessionFactory.build()
        payload_data = {"book": book.id}

        response = api_client.post(self.create_url, data=payload_data)
        response_2 = api_client.post(self.create_url, data=payload_data)

        assert response_2.status_code == status.HTTP_400_BAD_REQUEST
        assert response_2.data["non_field_errors"][0] == error_message

    @pytest.mark.freeze_time("2023-10-22T00:00:00Z")
    def test_start_reading_session_with_already_started_another_reading_session(
        self, user, api_client, freezer
    ):
        api_client.force_authenticate(user)
        book_1 = BookFactory()
        book_2 = BookFactory()

        proto_reading_session_1 = ReadingSessionFactory.build()
        payload_data_1 = {"book": book_1.id}

        proto_reading_session_2 = ReadingSessionFactory.build()
        payload_data_2 = {"book": book_2.id}

        response = api_client.post(self.create_url, data=payload_data_1)
        freezer.move_to("2023-10-22T01:53:00Z")
        response_2 = api_client.post(self.create_url, data=payload_data_2)

        assert response_2.status_code == status.HTTP_201_CREATED, response.data
        assert response_2.data["book"]["id"] == book_2.id
        assert response_2.data["user"]["id"] == user.id
        assert response_2.data["start_reading_session"] == "2023-10-22T01:53:00Z"

        reading_session = ReadingSession.objects.get(id=response.data["id"])
        assert not reading_session.is_active
        assert str(reading_session.duration_of_session) == "1:53:00"

    @pytest.mark.freeze_time("2023-10-22T00:00:00Z")
    def test_end_reading_session_happy(self, user, api_client, freezer):
        api_client.force_authenticate(user)

        reading_session = ReadingSessionFactory(user=user)

        freezer.move_to("2023-10-22T01:53:00Z")
        url = reverse(
            "api:booktimetracker:reading_sessions-end-reading-session",
            kwargs={"pk": reading_session.pk},
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["end_reading_session"] == "2023-10-22T01:53:00Z"
        assert response.data["duration_of_session"] == "01:53:00"
        assert not response.data["is_active"]

    @pytest.mark.freeze_time("2023-10-22T00:00:00Z")
    def test_end_reading_session_bad(self, user, api_client, freezer):
        api_client.force_authenticate(user)
        permission_error = "You do not have permission to perform this action."

        reading_session = ReadingSessionFactory()

        freezer.move_to("2023-10-22T01:53:00Z")
        url = reverse(
            "api:booktimetracker:reading_sessions-end-reading-session",
            kwargs={"pk": reading_session.pk},
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == permission_error
