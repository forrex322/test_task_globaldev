import datetime

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

from booktimetracker.models import Book, ReadingSession
from booktimetracker.utils import time_diff
from users.serializers import UserShortSerializer


class ListBookSerializer(serializers.ModelSerializer):
    """
    Serializer that uses for get list of books.
    """

    total_reading_time = serializers.CharField()

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "date_of_publication",
            "short_description",
            "total_reading_time",
        )


class RetrieveBookSerializer(serializers.ModelSerializer):
    """
    Serializer that uses for get certain book.
    """

    date_of_last_reading = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "date_of_publication",
            "short_description",
            "full_description",
            "date_of_last_reading",
        )

    @staticmethod
    def get_date_of_last_reading(obj):
        return ReadingSession.objects.filter(book=obj).last().start_reading_session


class CreateReadingSession(serializers.ModelSerializer):
    """
    Seralizer for creating new reading session.
    """

    user = serializers.HiddenField(default=CurrentUserDefault())
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), required=True, allow_null=False, allow_empty=False
    )

    class Meta:
        model = ReadingSession
        fields = (
            "id",
            "start_reading_session",
            "user",
            "book",
        )
        write_only_fields = ("user", "book")

    def to_representation(self, instance):
        self.fields["book"] = RetrieveBookSerializer()
        self.fields["user"] = UserShortSerializer()
        return super().to_representation(instance)

    def validate(self, attrs):
        user = attrs["user"]
        book = attrs["book"]

        if ReadingSession.objects.filter(user=user, book=book, is_active=True).exists():
            raise ValidationError(
                _(
                    "You can't start a new reading session, because old one isn't closed."
                )
            )

        sessions = ReadingSession.objects.filter(user=user, is_active=True)
        if sessions.exists():
            now = datetime.datetime.now()
            for session in sessions:
                session.is_active = False
                session.end_reading_session = now
                session.duration_of_session = time_diff(
                    datetime.datetime.strftime(now, "%H:%M"),
                    datetime.datetime.strftime(session.start_reading_session, "%H:%M"),
                )
                session.save()

        return attrs


class RetrieveReadingSessionSerializer(serializers.ModelSerializer):
    """
    Serializer to get details of reading session.
    """

    class Meta:
        model = ReadingSession
        fields = (
            "id",
            "user",
            "book",
            "start_reading_session",
            "end_reading_session",
            "duration_of_session",
            "is_active",
        )
