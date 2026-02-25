from django.conf import settings
from django.db import models


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=100, blank=True)
    publication_year = models.IntegerField(null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="добавил пользователь",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "books"
        verbose_name = "книга"
        verbose_name_plural = "книги"
