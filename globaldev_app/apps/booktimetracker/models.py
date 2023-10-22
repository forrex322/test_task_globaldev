from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Sum, Q
from django.utils.translation import ugettext_lazy as _


class BookQuerySet(models.QuerySet):
    def annotate_total_reading_time(self, user):
        return self.annotate(
            total_reading_time=Sum(
                "readingsession__duration_of_session",
                filter=Q(readingsession__user=user),
            ),
        )


class Book(models.Model):
    """
    Model for books.
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=150, help_text=_("Name of book")
    )
    author = models.CharField(
        verbose_name=_("Author"), max_length=150, help_text=_("Author of book")
    )
    date_of_publication = models.DateField(
        verbose_name=_("Date of publication of book"), help_text=_("Author of book")
    )
    short_description = models.CharField(
        verbose_name=_("Short description"),
        max_length=150,
        help_text=_("Short description of book"),
    )
    full_description = models.TextField(
        verbose_name=_("Full description"),
        validators=[MaxLengthValidator(500)],
        help_text=_("Full description of book"),
    )

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return self.name


class ReadingSession(models.Model):
    """
    Model for reading sessions.
    """

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User"),
        related_name="reading_sessions",
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        to="Book", verbose_name=_("Book"), null=True, on_delete=models.SET_NULL
    )
    start_reading_session = models.DateTimeField(
        verbose_name=_("Start of reading"), auto_now_add=True
    )
    end_reading_session = models.DateTimeField(
        verbose_name=_("End of reading"), null=True
    )
    duration_of_session = models.DurationField(
        verbose_name=_("Duration of reading session"), null=True
    )
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=True)

    def __str__(self):
        return f"Sessions number: {self.id} for {self.book.name}"
