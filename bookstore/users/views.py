from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import RegisterForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
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

            login(request, user)
            messages.success(request, f"Добро пожаловать, {username}!")

            url = reverse("homepage:book_list")
            return redirect(url)
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
