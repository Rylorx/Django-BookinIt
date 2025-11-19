from . import views
from django.urls import path


urlpatterns = [
    path("", views.books_view, name="books_view"),
    path("add_to_shelf/<int:book_id>/<str:status>/", views.add_to_shelf, name="add_to_shelf"),
    path("remove_from_shelf/<int:book_id>/<str:status>/", views.remove_from_shelf, name="remove_from_shelf"),
]
