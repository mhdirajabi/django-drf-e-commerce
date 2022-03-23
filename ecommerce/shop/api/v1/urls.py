from django.urls import path

from .views import (
    CancelPaidCartView,
    CartRetrieveCreateView,
    DeleteCartView,
    NotPaidCartView,
    PaidCartView,
    PayCartView,
    ProductListView,
    ShopListView,
    ShopTypeListView,
)

urlpatterns = [
    path(
        "shops/",
        ShopListView.as_view(),
        name="confirmed_shops_list",
    ),
    path("shop-types/", ShopTypeListView.as_view()),
    path(
        "shop/<int:shop_pk>/products/",
        ProductListView.as_view(),
        name="shop_products",
    ),
    path(
        "shop/<int:shop_pk>/cart/",
        CartRetrieveCreateView.as_view(),
        name="cart_retrieve_create",
    ),
    path(
        "shop/<int:shop_pk>/delete-cart/",
        DeleteCartView.as_view(),
        name="delete_cart",
    ),
    path(
        "shop/<int:shop_pk>/cart/<int:pk>/payment/",
        PayCartView.as_view(),
        name="cart_payment",
    ),
    path(
        "shop/<int:shop_pk>/cancel-cart/<int:pk>/",
        CancelPaidCartView.as_view(),
        name="cart_cancellation",
    ),
    path(
        "not-paid-carts/",
        NotPaidCartView.as_view(),
        name="not_paid_carts",
    ),
    path(
        "paid-carts/",
        PaidCartView.as_view(),
        name="paid_carts",
    ),
]
