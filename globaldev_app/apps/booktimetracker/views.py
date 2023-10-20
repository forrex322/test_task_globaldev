from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from booktimetracker.models import Book
from booktimetracker.serializers import ListBookSerializer, RetrieveBookSerializer


class BookViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveBookSerializer
        return ListBookSerializer
