from cart.models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key, user__isnull=True
        )
    return cart


def transfer_guest_cart_to_user(request, user):
    if not request.session.session_key:
        return

    try:
        guest_cart = Cart.objects.get(
            session_key=request.session.session_key, user__isnull=True
        )

        user_cart, _ = Cart.objects.get_or_create(user=user)

        for guest_item in guest_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                book=guest_item.book,
                defaults={"quantity": guest_item.quantity},
            )

            if not created:
                user_item.quantity += guest_item.quantity
                user_item.save()

        guest_cart.delete()

    except Cart.DoesNotExist:
        pass
