from pathlib import Path

AUTH_USER_MODEL = "users.User"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    "django-insecure-so2%a8ol+wtph&j-rt%0#gbun4_^-+47quwj7&nf1=3ak_j+jd"
)

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cart.apps.CartConfig",
    "homepage.apps.HomepageConfig",
    "orders.apps.OrdersConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookstore.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bookstore_db",
        "USER": "root",
        "PASSWORD": "root_secret_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            + ".MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

LOGIN_URL = "users:login"

LOGIN_REDIRECT_URL = "homepage:book_list"

LOGOUT_REDIRECT_URL = "homepage:book_list"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
