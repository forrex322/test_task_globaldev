from rest_framework import serializers

from booktimetracker.models import Book


class ListBookSerializer(serializers.ModelSerializer):
    """
    Serializer that uses for get list of books.
    """

    class Meta:
        model = Book
        fields = ("id", "name", "author", "date_of_publication", "short_description")


class RetrieveBookSerializer(serializers.ModelSerializer):
    """
    Serializer that uses for get certain book.
    """

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "date_of_publication",
            "short_description",
            "full_description",
            # "date_of_last_reading",
        )
