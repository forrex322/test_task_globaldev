from factory import (
    DjangoModelFactory,
    Faker,
    PostGenerationMethodCall,
    SubFactory,
    post_generation,
)

from users.tests.factories import UserFactory


class BookFactory(DjangoModelFactory):
    name = Faker("sentence")
    author = Faker("name")
    date_of_publication = Faker("date")
    short_description = Faker(
        "word",
    )
    full_description = Faker("text", max_nb_chars=500)

    class Meta:
        model = "booktimetracker.Book"


class ReadingSessionFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    book = SubFactory(BookFactory)

    class Meta:
        model = "booktimetracker.ReadingSession"
