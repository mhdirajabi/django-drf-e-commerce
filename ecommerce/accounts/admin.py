from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Address, CustomUser, Profile, TOTPRequest

# Register your models here.


admin.site.site_header = "پروژه فروشگاه اینترنتی - مدیریت کل سایت"


admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_salesman",
        "is_staff",
        "is_active",
        "passed_phone_number_verification",
    )
    list_filter = (
        "is_superuser",
        "is_salesman",
        "is_active",
        "passed_phone_number_verification",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password",
                    "is_salesman",
                    "passed_phone_number_verification",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_salesman",
                    "is_staff",
                    "is_active",
                    "passed_phone_number_verification",
                ),
            },
        ),
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    ordering = (
        "first_name",
        "last_name",
    )


admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    ordering = ("id",)


admin.site.register(Profile, ProfileAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "address",
        "user",
    )
    list_filter = (
        "city",
        "user",
    )
    search_fields = (
        "city",
        "address",
    )
    ordering = ("city",)


admin.site.register(Address, AddressAdmin)


class TOTPRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_id",
        "channel",
        "receiver",
        "code",
        "created",
    )
    ordering = ("-created",)


admin.site.register(TOTPRequest, TOTPRequestAdmin)
