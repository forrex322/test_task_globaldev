from django.contrib import admin

from booktimetracker.models import Book, ReadingSession


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "author",
        "date_of_publication",
        "short_description",
        "full_description",
    ]


@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "book",
        "start_reading_session",
        "end_reading_session",
        "duration_of_session",
        "is_active",
    ]
