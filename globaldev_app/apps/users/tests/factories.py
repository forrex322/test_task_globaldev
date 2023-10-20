from django.db.models.signals import post_save
from factory import (
    DjangoModelFactory,
    Faker,
    PostGenerationMethodCall,
    SubFactory,
    post_generation,
)
from factory.django import mute_signals

USER_PASSWORD = "SecretPassword1"


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = PostGenerationMethodCall("set_password", USER_PASSWORD)

    class Meta:
        model = "users.User"
        django_get_or_create = ("email",)


@mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    description = Faker("sentence", nb_words=4)
    birth_date = Faker("date_of_birth", maximum_age=100)

    class Meta:
        model = "users.Profile"
        django_get_or_create = ("user",)
