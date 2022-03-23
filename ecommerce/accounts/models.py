import uuid
from datetime import timedelta

import requests
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomerManager, CustomUserManager, SellerManager
from .utils import generate_totp, unique_slugify


class CustomUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField("آدرس ایمیل", unique=True)
    phone_number = PhoneNumberField("شماره موبایل", unique=True)
    first_name = models.CharField("نام", max_length=150)
    last_name = models.CharField("نام خانوادگی", max_length=150)
    is_staff = models.BooleanField("کارمند", default=False)
    is_active = models.BooleanField("فعال", default=True)
    is_salesman = models.BooleanField(
        "فروشنده",
        default=False,
        help_text="اگر مایل به ثبت فروشگاه و همکاری با مکتب هستید این تیک را بزنید.",
    )
    passed_phone_number_verification = models.BooleanField(
        "شماره موبایل تأیید شده؟", default=False
    )
    date_joined = models.DateTimeField("تاریخ پیوستن", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    sellers = SellerManager()
    customers = CustomerManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر"

    def __str__(self):
        return f"{self.email} | {self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=CASCADE,
        related_name="profile",
        verbose_name="کاربر",
    )
    bio = models.TextField("درباره من", blank=True, null=True)
    profile_pic = models.ImageField(
        "عکس پروفایل", null=True, blank=True, upload_to="images/profile_pictures"
    )
    slug = models.SlugField("اسلاگ", null=True, blank=True, allow_unicode=True)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌"

    def __str__(self):
        return f"""پروفایل کاربری | {self.user.email} |
                 {self.user.first_name} {self.user.last_name}"""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(
                self,
                slugify(
                    f"{self.user.first_name}-{self.user.last_name}", allow_unicode=True
                ),
            )
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Profile(user=user)
            user_profile.save()

    post_save.connect(create_profile, sender=CustomUser)


class Address(models.Model):
    city = models.CharField("شهر", max_length=50)
    address = models.TextField("آدرس")
    zip_code = models.CharField("کدپستی", max_length=10)
    user = models.ForeignKey(
        CustomUser,
        on_delete=SET_NULL,
        related_name="addresses",
        verbose_name="کاربر",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌"

    def __str__(self):
        return self.city + "، " + self.address


class TOTPRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, code):
        current_time = timezone.now()
        result = self.filter(
            receiver=receiver,
            request_id=request,
            code=code,
            created__lt=current_time,
            created__gt=current_time - timedelta(seconds=300),
        ).exists()
        return result


class TOTPManager(models.Manager):
    def get_queryset(self):
        return TOTPRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, code):
        return self.get_queryset().is_valid(receiver, request, code)

    def generate(self, data):
        totp = self.model(channel=data["channel"], receiver=data["receiver"])
        totp.save(using=self._db)
        return totp


class TOTPRequest(models.Model):
    class TOTPChannel(models.TextChoices):
        PHONE = "phone_number"

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    channel = models.CharField(
        "از طریق", max_length=20, choices=TOTPChannel.choices, default=TOTPChannel.PHONE
    )
    receiver = models.CharField("دریافت‌کننده", max_length=20)
    code = models.CharField("کد یکبار مصرف", max_length=4, default=generate_totp)
    created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True, editable=False)

    objects = TOTPManager()

    class Meta:
        verbose_name = "درخواست‌های رمز یکبار مصرف"
        verbose_name_plural = "درخواست‌های رمز یکبار مصرف"

    def send_totp(sender, **kwargs):
        request = kwargs["instance"]
        if kwargs["created"]:
            print("salam")
            API_KEY = "6569574E374562744E37733236305A7053635A364E6E536C4E3363655067683869553355733751496F616F3D"
            body = {
                "receptor": request.receiver,
                "token": request.code,
                "template": "verify",
            }
            requests.get(
                f"https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json",
                params=body,
            )

    post_save.connect(send_totp, sender="accounts.TOTPRequest")
