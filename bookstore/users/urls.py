from django.urls import path

from users.views import (
    check_email_ajax,
    login_view,
    logout_view,
    profile_view,
    register,
)

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("register/", register, name="register"),
    path("check-email/", check_email_ajax, name="check_email"),
]
