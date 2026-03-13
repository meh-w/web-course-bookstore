from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="email",
        help_text="введите email существующего сервиса.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "user"

        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("такой email уже используется.")
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            User.objects.exclude(pk=self.instance.pk)
            .filter(email=email)
            .exists()
        ):
            raise forms.ValidationError("такой email уже используется.")
        return email
