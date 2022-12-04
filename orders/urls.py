from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="orders"),
    path("order/<uuid:pk>", views.OrderDetailView.as_view(), name="order"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("remove-order-item/<uuid:order_item_id>/", views.remove_order_item, name="remove_order_item"),
    path("update-order-items-count/", views.update_order_items_count, name="update_order_items_count"),
    path("apply-coupon/", views.apply_coupon_to_order, name="apply_coupon"),
    path("add-product-to-cart/", views.add_product_to_cart, name="add-product-to-cart"),
]
