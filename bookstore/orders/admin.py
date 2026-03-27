from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book_title", "price", "quantity", "get_cost")
    fields = ("book_title", "price", "quantity", "get_cost")

    def get_cost(self, obj):
        return f"{obj.get_cost()} ₽"

    get_cost.short_description = "Сумма"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total_cost", "item_count")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "user__email", "id")
    readonly_fields = ("created_at", "total_cost")
    inlines = [OrderItemInline]

    fieldsets = (
        (
            "Информация о заказе",
            {"fields": ("user", "created_at", "total_cost")},
        ),
    )

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Товаров"

    def total_cost(self, obj):
        return f"{obj.total_cost} ₽"

    total_cost.short_description = "Общая стоимость"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "book_title",
        "price",
        "quantity",
        "get_cost",
    )
    list_filter = ("order__created_at",)
    search_fields = ("book_title", "order__id")
    readonly_fields = ("book_title", "price", "quantity", "get_cost")

    def get_cost(self, obj):
        return f"{obj.get_cost()} ₽"

    get_cost.short_description = "Сумма"
