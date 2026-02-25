from django.contrib import admin

from homepage.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        Book.id.field.name,
        Book.title.field.name,
        Book.author.field.name,
        Book.price.field.name,
        Book.publication_year.field.name,
        Book.added_by.field.name,
    )

    list_display_links = (
        Book.id.field.name,
        Book.title.field.name,
    )

    search_fields = (
        Book.title.field.name,
        Book.author.field.name,
    )

    list_filter = (
        Book.genre.field.name,
        Book.publication_year.field.name,
    )
