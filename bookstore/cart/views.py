from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.models import CartItem
from cart.utils import get_or_create_cart
from homepage.models import Book


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/cart_items.html", {"cart": cart})


@require_POST
def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, book=book, defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество "{book.title}" увеличено')
    else:
        messages.success(request, f'"{book.title}" добавлена в корзину')

    return redirect("homepage:book_list")


@require_POST
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Количество обновлено")
    else:
        cart_item.delete()
        messages.success(request, "Товар удален из корзины")

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    book_title = cart_item.book.title
    cart_item.delete()
    messages.success(request, f'"{book_title}" удалена из корзины')
    return redirect("cart:cart_detail")
