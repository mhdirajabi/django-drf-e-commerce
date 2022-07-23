from accounts.models import CustomUser as User
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from shop_management.models import Product

from .managers import CancelledCartsManager, OtherCartsManager, PaidCartsManager


class Cart(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "تأیید شده"),
        ("processing", "در حال بررسی"),
        ("cancelled", "کنسل شده"),
        ("paid", "پرداخت شده"),
    ]
    status = models.CharField(
        "وضعیت", choices=STATUS_CHOICES, default="processing", max_length=50
    )
    products = models.ManyToManyField(Product, through="CartItem")
    shop = models.ForeignKey(
        "shop_management.Shop",
        on_delete=CASCADE,
        null=True,
        verbose_name="فروشگاه",
        related_name="carts",
    )
    customer = models.ForeignKey(
        User, on_delete=CASCADE, verbose_name="مشتری", related_name="carts"
    )
    date_ordered = models.DateTimeField("تاریخ خرید", auto_now=True)

    objects = models.Manager()
    paid = PaidCartsManager()
    cancelled = CancelledCartsManager()
    other = OtherCartsManager()

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید"

    def __str__(self):
        return f"سبد خرید {self.id} | {self.customer}"

    def get_absolute_url(self):
        return reverse("cart_detail", kwargs={"pk": self.id})

    @property
    def total_price(self):
        cart_items = self.cart_items.all()
        total_price = sum([item.total for item in cart_items])
        return total_price

    @property
    def number_of_items(self):
        cart_items = self.cart_items.all()
        number_of_items = sum([item.quantity for item in cart_items])
        return number_of_items


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=CASCADE,
        verbose_name="سبد",
        related_name="cart_items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=SET_NULL,
        null=True,
        verbose_name="محصول",
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField("تعداد", default=1)
    price = models.PositiveIntegerField("قیمت", blank=True)

    class Meta:
        verbose_name = "آیتم سبد"
        verbose_name_plural = "آیتم سبد"

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.product.price
        return super().save(*args, **kwargs)

    @property
    def total(self):
        return self.price * self.quantity
