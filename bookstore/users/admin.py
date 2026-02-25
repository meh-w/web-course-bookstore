from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        User.id.field.name,
        User.username.field.name,
        User.email.field.name,
        User.first_name.field.name,
        User.role.field.name,
    )
    list_display_links = (
        User.id.field.name,
        User.username.field.name,
    )

    fieldsets = (
        (None, {"fields": (User.username.field.name, "password")}),
        (
            "Personal info",
            {
                "fields": (
                    User.first_name.field.name,
                    User.email.field.name,
                    User.role.field.name,
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    User.username.field.name,
                    User.email.field.name,
                    User.first_name.field.name,
                    User.role.field.name,
                    "password1",
                    "password2",
                ),
            },
        ),
    )
