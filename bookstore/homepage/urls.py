from django.urls import path

from homepage.views import book_add, book_edit, book_delete, book_list

app_name = "homepage"

urlpatterns = [
    path("", book_list, name="book_list"),
    path("book/add/", book_add, name="book_add"),
    path("book/<int:book_id>/delete/", book_delete, name="book_delete"),
    path("book/<int:book_id>/edit/", book_edit, name="book_edit"),
]
