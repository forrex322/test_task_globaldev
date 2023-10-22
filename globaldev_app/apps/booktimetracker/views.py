import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from booktimetracker.models import Book, ReadingSession
from booktimetracker.serializers import (
    ListBookSerializer,
    RetrieveBookSerializer,
    CreateReadingSession,
    RetrieveReadingSessionSerializer,
)
from booktimetracker.utils import time_diff
from users.permissions import IsOwner


class BookViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    Api viewset to get list of books and retrieve details of certain book.
    """

    queryset = Book.objects.prefetch_related("readingsession_set")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveBookSerializer
        return ListBookSerializer

    def get_queryset(self):
        return self.queryset.annotate_total_reading_time(user=self.request.user)


class ReadingSessionViewSet(GenericViewSet, CreateModelMixin):
    """
    Api viewset to create and end reading session.
    """

    queryset = ReadingSession.objects.all()
    serializer_class = CreateReadingSession
    permission_classes = [IsAuthenticated, IsOwner]

    @action(methods=["delete"], detail=True)
    def end_reading_session(self, request, *args, **kwargs):
        """
        Custom endpoint to end reading session.
        """
        instance = self.get_object()
        now = datetime.datetime.now()

        ReadingSession.objects.filter(id=instance.id, is_active=True).update(
            is_active=False,
            end_reading_session=now,
            duration_of_session=time_diff(
                datetime.datetime.strftime(now, "%H:%M"),
                datetime.datetime.strftime(instance.start_reading_session, "%H:%M"),
            ),
        )

        return Response(
            data=RetrieveReadingSessionSerializer(
                instance=self.get_object(), context=self.get_serializer_context()
            ).data,
            status=status.HTTP_200_OK,
        )
