from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Cart, CartItem
from shop_management.models import Product, Shop, ShopType

from .filters import ProductFilter
from .serializers import (
    CarItemCreateSerializer,
    CartItemSerializer,
    CartSerializer,
    DeleteCartItemSerializer,
    ProductSerializer,
    ShopSerializer,
    ShopTypeSerializer,
)


class ShopListView(ListAPIView):
    queryset = Shop.confirmed.all()
    serializer_class = ShopSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("type",)


class ShopTypeListView(ListAPIView):
    queryset = ShopType.objects.all()
    serializer_class = ShopTypeSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        return Product.objects.filter(shop=shop)


class CartRetrieveCreateView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        cart = get_object_or_404(Cart.other, shop=shop, customer=self.request.user)
        queryset = CartItem.objects.filter(cart=cart)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CartItemSerializer
        elif self.request.method == "POST":
            return CarItemCreateSerializer

    def create(self, request, *args, **kwargs):
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        product_id = request.data["product"]
        if product_id:
            product = get_object_or_404(Product, id=product_id, shop__id=shop_pk)
            if product.is_available:
                if product.stock >= 1:
                    try:
                        cart = get_object_or_404(
                            Cart.other, shop=shop, customer=self.request.user
                        )
                    except:
                        cart = Cart.objects.create(
                            shop=shop, customer=self.request.user
                        )
                    if cart.cart_items.filter(product__id=product_id).exists():
                        cart_item = cart.cart_items.get(product__id=product_id)
                        cart_item.quantity += 1
                        cart_item.save()
                        return Response(
                            {"Success": "سبد بروزرسانی شد"}, status=status.HTTP_200_OK
                        )
                    else:
                        request.data["cart"] = cart.id
                        serializer = self.get_serializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers,
                        )
                else:
                    return Response(
                        {"Error": "موجودی کالای انتخابی کافی نیست"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"Error": "موجودی این کالا به اتمام رسیده"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Error": "کالایی وارد نشده است"}, status=status.HTTP_400_BAD_REQUEST
        )


class DeleteCartView(APIView):
    queryset = CartItem.objects.all()
    serializer_class = DeleteCartItemSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=DeleteCartItemSerializer)
    def delete(self, request, *args, **kwargs):
        serializer = DeleteCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        cart = get_object_or_404(Cart.other, shop=shop, customer=self.request.user)
        if cart:
            if cart.cart_items.filter(product__id=serializer.data["product"]).exists():
                cart_item = cart.cart_items.get(product__id=serializer.data["product"])
                if cart_item.quantity == 1:
                    cart_item.delete()
                    if len(cart.cart_items.all()) <= 0:
                        cart.delete()
                        return Response(
                            {"Success": "سبد خرید با موفقیت حذف شد"},
                            status=status.HTTP_204_NO_CONTENT,
                        )
                    return Response(
                        {"Success": "آیتم مورد نظر با موفقیت از سبد حذف شد"},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    cart_item.quantity -= 1
                    cart_item.save()
                    return Response(
                        {"Success": "آیتم مورد نظر با موفقیت از سبد حذف شد"},
                        status=status.HTTP_204_NO_CONTENT,
                    )
            return Response(
                {"Error": "آیتم مورد نظر در سبد موجود نیست"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Error": "سبد فعالی یافت نشد"}, status=status.HTTP_400_BAD_REQUEST
        )


class PayCartView(UpdateAPIView):
    http_method_names = [
        "patch",
    ]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        queryset = Cart.other.filter(shop=shop, customer=self.request.user)
        return queryset

    def patch(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_items = cart.cart_items.all()
        for item in cart_items:
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()
            else:
                return Response(
                    {"Error": "تعداد برخی کالاهای انتخابی از موجودی کالا بیشتر است"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        cart.status = "paid"
        cart.save()
        return Response({"Success": "پرداخت انجام شد"}, status=status.HTTP_202_ACCEPTED)


class CancelPaidCartView(UpdateAPIView):
    queryset = Cart.paid.all()
    http_method_names = [
        "patch",
    ]
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        shop_pk = self.kwargs.get("shop_pk")
        shop = get_object_or_404(Shop.confirmed, id=shop_pk)
        obj = get_object_or_404(Cart.paid, shop=shop, customer=self.request.user)
        return obj

    def patch(self, *args, **kwargs):
        cart = self.get_object()
        cart_items = cart.cart_items.all()
        for item in cart_items:
            item.product.stock += item.quantity
            item.product.save()
        cart.status = "cancelled"
        cart.save()
        return Response({"Success": "خرید لغو شد"}, status=status.HTTP_200_OK)


class NotPaidCartView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return get_list_or_404(
            Cart.objects.filter(customer=self.request.user).exclude(status="paid")
        )


class PaidCartView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        return get_list_or_404(Cart.paid.filter(customer=self.request.user))
