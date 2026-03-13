from django.conf import settings
from django.db import models

from homepage.models import Book


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="пользователь",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания"
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at.strftime('%d.%m.%Y')}"

    @property
    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="заказ",
    )

    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, verbose_name="книга"
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="цена на момент заказа"
    )

    quantity = models.PositiveIntegerField(verbose_name="количество")

    book_title = models.CharField(
        max_length=255, verbose_name="название книги"
    )

    class Meta:
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"

    def __str__(self):
        return f"{self.book_title} x {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
