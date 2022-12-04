from django.contrib import admin

from .models import Order, OrderItem, OrderCoupon


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "is_paid", "payment_time"]
    list_editable = ["is_paid"]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "final_price", "count"]
    list_editable = ["count"]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderCoupon)
