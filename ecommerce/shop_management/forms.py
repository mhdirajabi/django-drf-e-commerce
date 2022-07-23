from django import forms

from .models import Product, Shop


class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = (
            "name",
            "type",
            "image",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام فروشگاه رو اینجا وارد کن...",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class UpdateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = (
            "name",
            "image",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class DeleteShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ()


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "brand",
            "description",
            "price",
            "stock",
            "image",
            "category",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام محصول",
                }
            ),
            "brand": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "برند",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "توضیحات",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "قیمت به تومان",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "موجودی کالا",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
