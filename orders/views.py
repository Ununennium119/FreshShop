import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from products.models import Product
from users.models import User
from .models import Order, OrderItem, OrderCoupon


@method_decorator(login_required, name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "orders/orders.html"

    def get_queryset(self):
        query = super(OrderListView, self).get_queryset()

        return query.filter(user_id=self.request.user.id)


@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order.html"


@method_decorator(login_required, name="dispatch")
class CartView(DetailView):
    model = Order
    template_name = "orders/cart.html"

    def get_object(self, queryset=None):
        query = queryset if queryset else self.get_queryset()
        order, created = query.get_or_create(is_paid=False, user_id=self.request.user.id)
        order.update_items_prices()
        return order


@login_required
def side_cart_component(request):
    order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    order.update_items_prices()

    context = {
        "order": order
    }
    return render(request, "orders/components/side_cart_component.html", context)


@login_required
def remove_order_item(request, order_item_id):
    response = {
        "status": "failed"
    }
    content_type = "application/json"

    if request.method == "DELETE":
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
        except OrderItem.DoesNotExist:
            return HttpResponse(json.dumps(response), content_type=content_type)

        if not order_item.order.is_paid and order_item.order.user.id == request.user.id:
            order_item.delete()
            response["status"] = "success"
            return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)


@login_required
def update_order_items_count(request):
    response = {
        "status": "failed"
    }
    content_type = "application/json"

    if request.method == "POST":
        user: User = User.objects.get(id=request.user.id)
        order, created = user.orders_set.get_or_create(is_paid=False)
        if created:
            return HttpResponse(json.dumps(response), content_type=content_type)

        items_counts = []
        try:
            body = json.loads(request.body.decode("utf-8"))
            order_items_count = body["order_items_counts"]
            for order_item_count in order_items_count:
                order_item_id = order_item_count["id"]
                order_item_count = int(order_item_count["count"])
                if order_item_count <= 0:
                    return HttpResponse(json.dumps(response), content_type=content_type)

                order_item = order.items_set.get(id=order_item_id)
                items_counts.append((order_item, order_item_count))

        except (json.JSONDecodeError, KeyError, TypeError, OrderItem.DoesNotExist):
            return HttpResponse(json.dumps(response), content_type=content_type)

        for order_item, order_item_count in items_counts:
            order_item.count = order_item_count
            order_item.save()

        response["status"] = "success"
        messages.success(request, "Quantities updated successfully!")
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)


@login_required
def apply_coupon_to_order(request):
    response = {
        "status": "failed",
        "message": "Failed to apply coupon!"
    }
    content_type = "application/json"

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            coupon_code = body["coupon_code"]
            coupon = OrderCoupon.objects.get(code=coupon_code, is_active=True)

        except (json.JSONDecodeError, KeyError, TypeError, OrderCoupon.DoesNotExist):
            return HttpResponse(json.dumps(response), content_type=content_type)

        user: User = User.objects.get(id=request.user.id)
        order, created = user.orders_set.get_or_create(is_paid=False)
        order.coupon = coupon
        order.save()

        response["status"] = "success"
        response["message"] = "Coupon applied successfully!"
        messages.success(request, "Coupon applied successfully!")
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)


def add_product_to_cart(request):
    response = {
        "status": "failed",
        "message": "Failed to add product to cart!"
    }
    content_type = "application/json"

    if request.method == "POST":
        if not request.user.is_authenticated:
            response["status"] = "login"
            response["message"] = "You need to login in order to add product to cart."
            response["login_path"] = reverse("login")
            messages.info(request, response["message"])
            return HttpResponse(json.dumps(response), content_type=content_type)

        try:
            body = json.loads(request.body.decode("utf-8"))
            product_id = body["productId"]
            quantity = int(body["quantity"])
            product = Product.objects.get(id=product_id, is_active=True)

        except (json.JSONDecodeError, KeyError, TypeError, Product.DoesNotExist):
            return HttpResponse(json.dumps(response), content_type=content_type)

        if quantity < 1 or quantity > 99:
            response["message"] = "Quantity must be between 1 to 99!"
            return HttpResponse(json.dumps(response), content_type=content_type)

        if product.available_quantity < quantity:
            response["message"] = "We don't have enough of this product!"
            return HttpResponse(json.dumps(response), content_type=content_type)

        user = User.objects.get(id=request.user.id)
        order, created = user.orders_set.get_or_create(is_paid=False)
        order_item, created = order.items_set.get_or_create(product_id=product_id, defaults={"count": quantity})
        order_item.count = quantity
        order_item.save()

        response["status"] = "success"
        if created:
            response["message"] = "Product added to cart successfully!"
        else:
            response["message"] = "Product was already in your cart. Quantity updated!"
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)
