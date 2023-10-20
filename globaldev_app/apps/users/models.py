import datetime

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Model of user for registration and login.
    """

    email = models.EmailField(_("email address"), unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()


class Profile(TimeStampedModel):
    """
    Profile of user what contains additional fields.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("related user"),
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    description = models.TextField(
        _("description of user's profile"), blank=True, default=""
    )
    birth_date = models.DateField(
        _("Date of birth"),
        validators=[
            MinValueValidator(datetime.date(1910, 1, 1)),
            MaxValueValidator(datetime.date.today),
        ],
        null=True,
        blank=True,
    )
    last_7_days_statistic = models.DurationField(null=True, blank=True)
    last_30_days_statistic = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"profile of user {self.user_id}"

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def full_name(self):
        return self.user.get_full_name()
