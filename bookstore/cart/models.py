from django.conf import settings
from django.db import models

from homepage.models import Book


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="пользователь",
    )

    session_key = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="ключ сессии"
    )

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "коризны"

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username}"
        return f"Корзина (гость, {self.session_key[:8]}...)"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="корзина",
    )

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name="книга"
    )

    quantity = models.PositiveIntegerField(
        default=1, verbose_name="количество"
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        unique_together = ["cart", "book"]

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    def get_cost(self):
        return self.book.price * self.quantity
