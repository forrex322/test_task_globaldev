from rest_framework.routers import SimpleRouter

from booktimetracker.views import BookViewSet

book_router = SimpleRouter()
book_router.register("books", BookViewSet, "books")


urlpatterns = book_router.urls
