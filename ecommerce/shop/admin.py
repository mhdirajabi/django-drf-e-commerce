from django.contrib import admin

from .models import Cart, CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "status",
        "date_ordered",
        "total_price",
        "number_of_items",
    )
    list_filter = ("status",)


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "total")
    list_filter = ("cart",)


admin.site.register(CartItem, CartItemAdmin)
