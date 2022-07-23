from accounts.models import CustomUser as User
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .managers import ConfirmedShopManager, ShopManager
from .utils import unique_slugify

# Create your models here.


class Shop(models.Model):
    STATUS_CHOICES = (
        ("confirmed", "تأیید شده"),
        ("rejected", "رد شده"),
        ("processing", "در حال بررسی"),
        ("deleted", "حذف شده"),
    )
    name = models.CharField("نام فروشگاه", max_length=200, unique=True)
    slug = models.SlugField("اسلاگ", null=True, blank=True, allow_unicode=True)
    status = models.CharField(
        "وضعیت", max_length=50, choices=STATUS_CHOICES, default="processing"
    )
    image = models.ImageField(
        "عکس فروشگاه",
        null=True,
        blank=True,
        upload_to="images/shop_images",
        help_text="ارسال عکس اختیاری است.",
    )
    type = models.ForeignKey(
        "ShopType",
        on_delete=SET_NULL,
        null=True,
        verbose_name="نوع فروشگاه",
        related_name="shops",
        help_text="در انتخاب این مورد دقت کنید، امکان تغییر نوع فروشگاه در آینده وجود نخواهد داشت.",
    )
    owner = models.ForeignKey(
        User, on_delete=CASCADE, verbose_name="صاحب فروشگاه", related_name="shops"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    last_updated = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    objects = models.Manager()
    available = ShopManager()
    confirmed = ConfirmedShopManager()

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌"

    def __str__(self):
        return f"{self.name} - {self.owner.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name, allow_unicode=True))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop_detail", kwargs={"slug": self.slug})


class ShopType(models.Model):
    name = models.CharField("نام", max_length=100)

    class Meta:
        verbose_name = "نوع فروشگاه"
        verbose_name_plural = "‌انواع فروشگاه‌"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("نام محصول", max_length=150)
    brand = models.CharField("برند", max_length=150, null=True, blank=True)
    description = models.TextField("توضیحات محصول", null=True, blank=True)
    price = models.PositiveIntegerField("قیمت محصول")
    stock = models.PositiveIntegerField("موجودی محصول")
    is_available = models.BooleanField("موجود بودن", default=True)
    image = models.ImageField(
        "عکس محصول", null=True, upload_to="images/product_images", blank=True
    )
    category = models.ForeignKey(
        "ProductCategory",
        on_delete=SET_NULL,
        null=True,
        verbose_name="دسته‌بندی محصول",
        related_name="products",
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=CASCADE,
        verbose_name="فروشگاه",
        related_name="products",
    )
    slug = models.SlugField("اسلاگ", null=True, blank=True, allow_unicode=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    last_updated = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول"

    def __str__(self):
        return f"{self.name} | {self.shop}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(
                self, slugify(f"{self.name}-{self.shop.name}", allow_unicode=True)
            )
        if not self.stock:
            self.is_available = False
        if self.stock > 0 and self.is_available == False:
            self.is_available = True
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    @property
    def get_stock(self):
        return self.stock

    def image_tag(self):
        if self.image:
            return mark_safe(
                """<img src='{:s}' style='width: 45px; height:45px;
                border-radius: 50%;
                margin-left: auto;
                margin-right: auto;'>""".format(
                    self.image.url
                )
            )
        else:
            return mark_safe(
                """<img
                src='https://i.postimg.cc/J7GdRGpn/no-image.jpg'
                style='width: 45px; height:45px;
                border-radius: 50%;
                margin-left: auto;
                margin-right: auto;'"""
            )

    image_tag.short_description = "عکس محصول"


class ProductCategory(models.Model):
    name = models.CharField("نام دسته‌بندی", max_length=150)
    slug = models.SlugField("اسلاگ", null=True, blank=True, allow_unicode=True)
    parent = models.ForeignKey(
        "self",
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="children",
        verbose_name="دسته‌بندی اصلی",
    )

    class Meta:
        # enforcing that there can not be two categories under
        # a parent with same slug

        unique_together = (
            "slug",
            "parent",
        )
        verbose_name = "دسته‌بندی محصول"
        verbose_name_plural = "دسته‌بندی محصول"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name, allow_unicode=True))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_category", kwargs={"slug": self.slug})
