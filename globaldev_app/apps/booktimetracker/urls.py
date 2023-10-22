from rest_framework.routers import SimpleRouter

from booktimetracker.views import BookViewSet, ReadingSessionViewSet

book_router = SimpleRouter()
book_router.register("books", BookViewSet, "books")

reading_session = SimpleRouter()
reading_session.register("reading_session", ReadingSessionViewSet, "reading_sessions")

urlpatterns = book_router.urls + reading_session.urls
