import datetime

from factory import (
    DjangoModelFactory,
    Faker,
    PostGenerationMethodCall,
    SubFactory,
    post_generation,
)


class BookFactory(DjangoModelFactory):
    name = Faker("sentence")
    author = Faker("name")
    # date_of_publication = Faker('date', end_datetime=datetime.date.today(),)
    date_of_publication = Faker("date")
    short_description = Faker(
        "word",
    )
    full_description = Faker("text", max_nb_chars=500)

    class Meta:
        model = "booktimetracker.Book"
