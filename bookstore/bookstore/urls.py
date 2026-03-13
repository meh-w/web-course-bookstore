from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("users/", include("users.urls")),
]
