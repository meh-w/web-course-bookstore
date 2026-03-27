from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from email_validator import validate_email, EmailNotValidError

from cart.utils import transfer_guest_cart_to_user
from users.forms import ProfileEditForm, RegisterForm
from users.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            transfer_guest_cart_to_user(request, user)
            login(request, user)

            if user.role == "admin":
                messages.success(request, "С возвращением, администратор!")
            else:
                messages.success(
                    request, f"С возвращением, {user.first_name}!"
                )
            url = reverse("homepage:book_list")
            return redirect(url)
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из системы")
    url = reverse("homepage:book_list")
    return redirect(url)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            transfer_guest_cart_to_user(request, user)
            login(request, user)

            messages.success(request, f"Добро пожаловать, {username}!")

            url = reverse("homepage:book_list")
            return redirect(url)
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileEditForm(
                request.POST,
                instance=request.user.__class__.objects.get(
                    pk=request.user.pk
                ),
            )
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "данные профиля успешно обновлены")
                return redirect("users:profile")
            password_form = PasswordChangeForm(request.user)

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "пароль успешно изменён")
                return redirect("users:profile")
            profile_form = ProfileEditForm(instance=request.user)
    else:
        profile_form = ProfileEditForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {"profile_form": profile_form, "password_form": password_form}
    return render(request, "users/profile.html", context)


def check_email_ajax(request):
    if request.method == "GET":
        email = request.GET.get("email", "").strip().lower()

        if not email:
            return JsonResponse({"valid": False, "message": "Введите email"})

        try:
            valid = validate_email(email, check_deliverability=True)
            normalized_email = valid.email.lower()
        except EmailNotValidError as e:
            print(f"Ошибка валидации: {e}")
            return JsonResponse({"valid": False, "message": str(e)})

        if User.objects.filter(email=normalized_email).exists():
            print(f"Email {normalized_email} уже существует")
            return JsonResponse(
                {"valid": False, "message": "Этот email уже зарегистрирован"}
            )

        print(f"Email {normalized_email} валидный и доступен")
        return JsonResponse({"valid": True, "message": "Email доступен"})

    return JsonResponse({"error": "Invalid request"}, status=400)
