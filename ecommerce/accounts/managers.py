from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from .querysets import TOTPRequestQuerySet


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("آدرس ایمیل باید وارد شود.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("کاربر مافوق باید تیک کارمند بودن را داشته باشد")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("کاربر مافوق باید تیک کاربر مافوق بودن را داشته باشد")
        return self.create_user(email, password, **extra_fields)


class SellerManager(CustomUserManager):
    def get_queryset(self):
        return (
            super(SellerManager, self)
            .get_queryset()
            .filter(is_superuser=False, is_staff=False, is_salesman=True)
        )


class CustomerManager(CustomUserManager):
    def get_queryset(self):
        return (
            super(CustomerManager, self)
            .get_queryset()
            .filter(is_superuser=False, is_staff=False, is_salesman=False)
        )


class TOTPManager(models.Manager):
    def get_queryset(self):
        return TOTPRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, code):
        return self.get_queryset().is_valid(receiver, request, code)

    def generate(self, data):
        totp = self.model(channel=data["channel"], receiver=data["receiver"])
        totp.save(using=self._db)
        return totp
