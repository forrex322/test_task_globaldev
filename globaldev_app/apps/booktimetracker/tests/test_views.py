import pytest

from django.urls import reverse
from rest_framework import status

from users.models import User
from booktimetracker.tests.factories import BookFactory

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

        url = reverse("api:booktimetracker:books-detail", kwargs={"pk": book.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == book.id
        assert response.data["name"] == book.name
        assert response.data["author"] == book.author
        assert response.data["date_of_publication"] == book.date_of_publication
        assert response.data["short_description"] == book.short_description
        assert response.data["full_description"] == book.full_description

        # assert response.data['reading_session']
