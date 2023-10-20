from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
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

    def __str__(self):
        return self.name
