from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from homepage.models import Book


def book_list(request):
    all_books = Book.objects.all().order_by("title")

    paginator = Paginator(all_books, 5)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "can_add": request.user.is_authenticated,
        "is_admin": request.user.is_authenticated
        and request.user.role == "admin",
    }

    return render(request, "homepage/main.html", context)


@login_required
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
            added_by=request.user,
        )

        url = reverse("homepage:book_list")
        return redirect(url)

    return render(request, "homepage/book_add_form.html")


@login_required
def book_edit(request, book_id):
    if request.user.role != "admin":
        messages.error(request, "У вас нет прав доступа для редактирования")
        return redirect("homepage:book_list")

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.genre = request.POST.get("genre", "")
        publication_year = request.POST.get("publication_year")
        book.publication_year = publication_year if publication_year else None

        book.save()

        url = reverse("homepage:book_list")
        return redirect(url)

    return render(request, "homepage/book_edit_form.html", {"book": book})


@login_required
def book_delete(request, book_id):
    if request.user.role != "admin":
        messages.error(request, "У вас нет прав доступа для удаления")
        return redirect("homepage:book_list")

    book = get_object_or_404(Book, id=book_id)
    book.delete()
    url = reverse("homepage:book_list")
    return redirect(url)
