from django.urls import path
from django.urls.conf import re_path

from .views import (
    CancelledCartsList,
    CartDetailView,
    CartListView,
    ConfirmedCartsList,
    CreateProductView,
    CreateShopView,
    CustomerListView,
    DeleteShopView,
    FilterCartsByCreationTime,
    PaidCartsList,
    ProcessingCartsList,
    ProductListView,
    ShopDetailView,
    ShopListView,
    UpdateShopView,
    chartview,
)

urlpatterns = [
    path("shops/", ShopListView.as_view(), name="shop_list"),
    path("create-new-shop/", CreateShopView.as_view(), name="create_shop"),
    re_path(
        "edit/shop/(?P<slug>[-\w]+)/", UpdateShopView.as_view(), name="update_shop"
    ),
    path(
        "shop/carts/<int:pk>/",
        CartDetailView.as_view(),
        name="cart_detail",
    ),
    re_path("^shop/(?P<slug>[-\w]+)/", ShopDetailView.as_view(), name="shop_detail"),
    re_path(
        "delete/shop/(?P<slug>[-\w]+)/", DeleteShopView.as_view(), name="delete_shop"
    ),
    re_path(
        "products/shop/(?P<slug>[-\w]+)/",
        ProductListView.as_view(),
        name="product_list",
    ),
    re_path(
        "add/products/(?P<slug>[-\w]+)/",
        CreateProductView.as_view(),
        name="create_product",
    ),
    re_path(
        "^carts/shop/(?P<slug>[-\w]+)/",
        CartListView.as_view(),
        name="cart_list",
    ),
    re_path(
        "processing-carts/shop/(?P<slug>[-\w]+)/",
        ProcessingCartsList.as_view(),
        name="processing_cart_list",
    ),
    re_path(
        "confirmed-carts/shop/(?P<slug>[-\w]+)/",
        ConfirmedCartsList.as_view(),
        name="confirmed_cart_list",
    ),
    re_path(
        "cancelled-carts/shop/(?P<slug>[-\w]+)/",
        CancelledCartsList.as_view(),
        name="cancelled_cart_list",
    ),
    re_path(
        "paid-carts/shop/(?P<slug>[-\w]+)/",
        PaidCartsList.as_view(),
        name="paid_cart_list",
    ),
    re_path(
        "time-filtered-carts/shop/(?P<slug>[-\w]+)/",
        FilterCartsByCreationTime.as_view(),
        name="filter_by_time",
    ),
    re_path(
        "customers/shop/(?P<slug>[-\w]+)/",
        CustomerListView.as_view(),
        name="customer_list",
    ),
    re_path("sale-reports/shop/(?P<slug>[-\w]+)/", chartview, name="sale_reports"),
]
