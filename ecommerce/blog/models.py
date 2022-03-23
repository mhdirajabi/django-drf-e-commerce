from accounts.models import CustomUser as User
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import slugify

from .utils import unique_slugify

# Create your models here.


class General(models.Model):
    content = models.TextField(verbose_name="متن")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(General):
    title = models.CharField("عنوان", max_length=100)
    creator = models.ForeignKey(
        User, on_delete=CASCADE, related_name="posts", verbose_name="نویسنده"
    )
    image = models.ImageField(
        "عکس", null=True, blank=True, upload_to="images/post_images"
    )
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)
    categories = models.ManyToManyField(
        "Category",
        db_table="Post_Categories",
        related_name="posts",
        verbose_name="دسته‌بندی‌ها",
    )
    tags = models.ManyToManyField(
        "Tag",
        db_table="Post_Tags",
        related_name="posts",
        verbose_name="تگ‌ها",
        blank=True,
    )

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "پست"
        verbose_name_plural = "پست"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title, allow_unicode=True))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})


class Category(models.Model):
    name = models.CharField("نام", max_length=200, unique=True)
    owner = models.ForeignKey(
        User, on_delete=CASCADE, related_name="categories", verbose_name="سازنده"
    )
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name, allow_unicode=True))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField("نام", max_length=100, unique=True)
    owner = models.ForeignKey(
        User, on_delete=CASCADE, related_name="tags", verbose_name="سازنده"
    )
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name, allow_unicode=True))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"slug": self.slug})
