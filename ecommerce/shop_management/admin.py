from django.contrib import admin

from .models import Product, ProductCategory, Shop, ShopType

# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "type",
        "status",
    )
    list_filter = (
        "status",
        "type",
    )
    list_editable = ("status",)
    search_fields = ("name",)
    ordering = (
        "status",
        "type",
        "owner",
    )
    actions = ["change_status"]

    @admin.action(
        description='تغییر وضعیت فروشگاه‌های\
        انتخاب شده به "تأیید شده"'
    )
    def change_status(self, request, queryset):
        queryset.update(status="confirmed")


admin.site.register(Shop, ShopAdmin)

admin.site.register(ShopType)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "shop", "price", "stock", "image_tag")
    list_filter = (
        "shop",
        "category",
    )
    search_fields = ("name",)
    ordering = (
        "shop",
        "name",
        "price",
        "stock",
    )


admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
    )
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent",)


admin.site.register(ProductCategory, ProductCategoryAdmin)
