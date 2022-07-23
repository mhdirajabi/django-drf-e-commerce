import datetime

from accounts.models import CustomUser as User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from shop.models import Cart

from .forms import CreateProductForm, CreateShopForm, DeleteShopForm, UpdateShopForm
from .mixins import IsSalesmanMixin
from .models import Product, Shop

# Create your views here.


class CreateShopView(LoginRequiredMixin, IsSalesmanMixin, CreateView):
    model = Shop
    form_class = CreateShopForm
    template_name = "shop_management/create_shop.html"

    def form_valid(self, form):
        if Shop.available.filter(owner=self.request.user).filter(status="processing"):
            messages.error(
                self.request,
                "برای ثبت فروشگاه جدید تا تأیید شدن فروشگاه‌های قبلی منتظر بمانید.",
            )
            return HttpResponseRedirect(reverse_lazy("shop_list"))
        form.instance.owner = self.request.user
        shop = form.save(commit=False)
        shop.save()
        messages.success(self.request, "فروشگاه با موفقیت ثبت شد.")
        return HttpResponseRedirect(reverse_lazy("shop_list"))


class ShopListView(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Shop
    template_name = "shop_management/shop_list.html"

    def get_queryset(self):
        return Shop.available.filter(owner=self.request.user).order_by("type")


class ShopDetailView(LoginRequiredMixin, IsSalesmanMixin, DetailView):
    model = Shop
    template_name = "shop_management/shop_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(shop=context["shop"])
        return context


class UpdateShopView(LoginRequiredMixin, IsSalesmanMixin, UpdateView):
    model = Shop
    form_class = UpdateShopForm
    template_name = "shop_management/update_shop.html"

    def form_valid(self, form):
        self.object.status = "processing"
        shop = form.save(commit=False)
        shop.save()
        messages.success(self.request, "فروشگاه با موفقیت بروزرسانی شد.")
        return HttpResponseRedirect(reverse_lazy("shop_list"))


class DeleteShopView(LoginRequiredMixin, IsSalesmanMixin, UpdateView):
    model = Shop
    form_class = DeleteShopForm
    template_name = "shop_management/delete_shop.html"

    def form_valid(self, form):
        self.object.status = "deleted"
        shop = form.save()
        shop.save()
        messages.warning(self.request, "فروشگاه با موفقیت حذف شد.")
        return HttpResponseRedirect(reverse_lazy("shop_list"))


class ProductListView(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Product
    template_name = "shop_management/product_list.html"

    def get_queryset(self):
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        print(shop)
        qs = shop.products.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context


class CreateProductView(LoginRequiredMixin, IsSalesmanMixin, CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = "shop_management/create_product.html"

    def form_valid(self, form):
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        form.instance.shop = shop
        product = form.save(commit=False)
        product.save()
        messages.success(self.request, "محصول با موفقیت ثبت شد.")
        return HttpResponseRedirect(
            reverse_lazy("product_list", kwargs={"slug": shop.slug})
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context


class CartListView(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/cart_list.html"

    def get_queryset(self):
        carts = Cart.objects.filter(
            cart_items__product__shop__slug=self.kwargs["slug"]
        ).distinct()
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = Cart.objects.filter(
            cart_items__product__shop__slug=self.kwargs["slug"]
        ).distinct()[int(cart_index)]
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class CartDetailView(LoginRequiredMixin, IsSalesmanMixin, DetailView):
    model = Cart
    template_name = "shop_management/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.cart_items.all()
        shop = items[0].product.shop
        context["shop"] = shop
        return context


class ProcessingCartsList(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/proccessing_cart_list.html"

    def get_queryset(self):
        carts = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="processing")
        )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="processing")[int(cart_index)]
        )
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class ConfirmedCartsList(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/confirmed_cart_list.html"

    def get_queryset(self):
        carts = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="confirmed")
        )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="confirmed")[int(cart_index)]
        )
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class CancelledCartsList(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/cancelled_cart_list.html"

    def get_queryset(self):
        carts = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="cancelled")
        )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="cancelled")[int(cart_index)]
        )
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class PaidCartsList(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/paid_cart_list.html"

    def get_queryset(self):
        carts = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="paid")
        )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(status="paid")[int(cart_index)]
        )
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class FilterCartsByCreationTime(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/filter_by_time.html"

    def get_queryset(self):
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        carts = (
            Cart.objects.filter(cart_items__product__shop__slug=self.kwargs["slug"])
            .distinct()
            .filter(date_ordered__range=[start, end])
        )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop"] = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["start"] = self.request.GET.get("start")
        context["end"] = self.request.GET.get("end")
        return context

    def post(self, request, *args, **kwargs):
        cart_index = request.POST.get("cart_index")
        cart = Cart.objects.filter(
            cart_items__product__shop__slug=self.kwargs["slug"]
        ).distinct()[int(cart_index)]
        cart.status = request.POST.get("value")
        cart.save()
        return JsonResponse({})


class CustomerListView(LoginRequiredMixin, IsSalesmanMixin, ListView):
    model = Cart
    template_name = "shop_management/customer_list.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        customers = User.customers.filter(carts__status="paid", carts__shop__slug=slug)
        carts = (
            Cart.paid.filter(customer__in=customers)
            .values("customer")
            .annotate(last_cart=Max("date_ordered"))
        )
        for cart in carts:
            customer_carts = Cart.paid.filter(customer=cart["customer"])
            cart["customer_fullname"] = (
                customer_carts[0].customer.first_name
                + " "
                + customer_carts[0].customer.last_name
            )
            cart["total_paid_carts"] = customer_carts.count()
            cart["all_time_total"] = sum(
                [cart_customer.total_price for cart_customer in customer_carts]
            )
            cart["all_time_number_of_items"] = sum(
                [cart_customer.number_of_items for cart_customer in customer_carts]
            )
        return carts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop.available, slug=self.kwargs["slug"])
        context["shop"] = shop
        print(context)
        return context


def chartview(request, slug):
    shop = get_object_or_404(Shop.available, slug=slug)
    sold_carts = (
        Cart.paid.filter(shop=shop)
        .values("date_ordered__month")
        .annotate(cart_count=Count("date_ordered__month"))
    )
    month_numbers = [item["date_ordered__month"] for item in sold_carts]
    months = []
    for i in month_numbers:
        obj = datetime.datetime.strptime(str(i), "%m")
        months.append(obj)
    context = {"shop": shop, "carts": sold_carts, "months": months}
    return render(request, "shop_management/sale_reports.html", context)
