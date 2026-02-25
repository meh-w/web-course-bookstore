from django.urls import path

import homepage.views

urlpatterns = [
    path("", homepage.views.book_list),
    path("book/add/", homepage.views.book_add),
    path("book/<int:book_id>/edit/", homepage.views.book_edit),
    path("book/<int:book_id>/delete/", homepage.views.book_delete),
]
