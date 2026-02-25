from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_email_domain


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "обычный пользователь"),
        ("admin", "администратор"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user",
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        verbose_name="email-адрес",
        help_text="введите email существующего сервиса.",
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
