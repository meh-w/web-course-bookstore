from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from cart.utils import get_or_create_cart
from orders.models import Order, OrderItem


@login_required
@require_POST
def order_create(request):
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.error(request, "Корзина пуста")
        return redirect("cart:cart_detail")

    order = Order.objects.create(user=request.user)

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            book=cart_item.book,
            price=cart_item.book.price,
            quantity=cart_item.quantity,
            book_title=cart_item.book.title,
        )

    cart.items.all().delete()

    messages.success(request, f"Заказ #{order.id} успешно оформлен")
    return redirect("orders:order_detail", order_id=order.id)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, "orders/order_list.html", {"orders": orders})
