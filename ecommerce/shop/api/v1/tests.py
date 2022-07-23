from accounts.models import CustomUser as User
from django.urls import reverse
from rest_framework.test import APITestCase
from shop.models import Cart, CartItem
from shop_management.models import Product, ProductCategory, Shop, ShopType


class TestShopping(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            email="testing@test.com",
            phone_number="09122233456",
            first_name="test",
            last_name="tested",
            password="some_strong_password",
        )
        self.seller = User.objects.create_user(
            email="testing2@test.com",
            phone_number="09122233457",
            first_name="test",
            last_name="testing",
            password="some_strong_password",
            is_salesman=True,
        )
        self.shop_type_1 = ShopType.objects.create(name="test_type")
        self.shop_type_2 = ShopType.objects.create(name="test_type2")
        self.shop_type_3 = ShopType.objects.create(name="test_type3")
        self.shop1 = Shop.objects.create(
            name="shop1",
            status="confirmed",
            type=self.shop_type_1,
            owner=self.seller,
        )
        self.shop2 = Shop.objects.create(
            name="shop2",
            status="confirmed",
            type=self.shop_type_2,
            owner=self.seller,
        )
        self.shop3 = Shop.objects.create(
            name="shop3",
            status="processing",
            type=self.shop_type_3,
            owner=self.seller,
        )
        self.shop4 = Shop.objects.create(
            name="shop4",
            status="confirmed",
            type=self.shop_type_3,
            owner=self.seller,
        )
        self.product_category = ProductCategory.objects.create(name="category")
        self.product = Product.objects.create(
            name="product",
            price=10000,
            stock=5,
            category=self.product_category,
            shop=self.shop1,
        )
        self.product2 = Product.objects.create(
            name="product2",
            price=5000,
            stock=10,
            category=self.product_category,
            shop=self.shop2,
        )
        self.cart = Cart.objects.create(shop=self.shop1, customer=self.customer)
        self.cart2 = Cart.objects.create(
            status="paid", shop=self.shop1, customer=self.customer
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product)

    def test_listed_shops_are_confirmed(self):
        response = self.client.get("/api-shop/shops/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_wrong_filter_on_confirmed_shops(self):
        url = "%s?type=supermarket" % reverse("confirmed_shops_list")
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 400)

    def test_shop_type_list(self):
        response = self.client.get("/api-shop/shop-types/")
        self.assertEqual(response.status_code, 200)

    def test_product_list(self):
        url = reverse("shop_products", kwargs={"shop_pk": self.shop1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_null_product_list(self):
        url = reverse("shop_products", kwargs={"shop_pk": self.shop4.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_cart(self):
        self.client.force_authenticate(self.customer)
        url = reverse("cart_retrieve_create", kwargs={"shop_pk": self.shop1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_cart(self):
        self.client.force_authenticate(self.customer)
        url = reverse("cart_retrieve_create", kwargs={"shop_pk": self.shop2.pk})
        response = self.client.post(
            url, format="json", data={"product": self.product2.pk}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["product"], self.product2.pk)
        response_2 = self.client.post(
            url, format="json", data={"product": self.product2.pk}
        )
        self.assertEqual(response_2.status_code, 200)
        response_3 = self.client.post(url, format="json", data={"product": ""})
        self.assertEqual(response_3.status_code, 400)

    def test_delete_cart(self):
        self.client.force_authenticate(self.customer)
        url = reverse("delete_cart", kwargs={"shop_pk": self.shop1.pk})
        response = self.client.delete(
            url, format="json", data={"product": self.product.pk}
        )
        self.assertEqual(response.status_code, 204)

    def test_cart_payment(self):
        self.client.force_authenticate(self.customer)
        url = reverse(
            "cart_payment",
            kwargs={"shop_pk": self.shop1.pk, "pk": self.cart.pk},
        )
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 202)

    def test_cart_cancellation(self):
        self.client.force_authenticate(self.customer)
        url = reverse(
            "cart_cancellation",
            kwargs={"shop_pk": self.shop1.pk, "pk": self.cart2.pk},
        )
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)

    def test_not_paid_carts_list(self):
        self.client.force_authenticate(self.customer)
        url = reverse("not_paid_carts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "processing")

    def test_paid_carts_list(self):
        self.client.force_authenticate(self.customer)
        url = reverse("paid_carts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "paid")
