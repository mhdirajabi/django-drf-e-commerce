from django_filters import rest_framework as filters
from shop_management.models import Product


class ProductFilter(filters.FilterSet):
    price__gt = filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Product
        fields = ["category", "is_available"]
