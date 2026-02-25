from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from homepage.models import Book


def book_list(request):
    all_books = Book.objects.all().order_by("title")

    paginator = Paginator(all_books, 5)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)

    return render(request, "homepage.html", {"page_obj": page_obj})


def book_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        price = request.POST.get("price")
        genre = request.POST.get("genre", "")
        publication_year = request.POST.get("publication_year")

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            genre=genre,
            publication_year=publication_year if publication_year else None,
        )

        return redirect("/")

    return render(request, "book_add_form.html")


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.genre = request.POST.get("genre", "")
        publication_year = request.POST.get("publication_year")
        book.publication_year = publication_year if publication_year else None

        book.save()

        return redirect("/")

    return render(request, "book_edit_form.html", {"book": book})


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("/")
