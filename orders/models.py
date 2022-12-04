import uuid

from django.db import models

from products.models import Product
from users.models import User


class OrderCoupon(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    code = models.CharField(max_length=64)
    discount_percentage = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_set")
    coupon = models.ForeignKey(OrderCoupon, on_delete=models.SET_NULL, related_name="orders_set", null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["is_paid", "-payment_time"]

    def __str__(self):
        return f"{self.user}'s order"

    @property
    def total_price(self):
        total = 0
        for order_item in self.items_set.all():
            total += order_item.total_price
        return round(total, 2)

    @property
    def coupon_discount(self):
        if self.coupon:
            return round(self.total_price * self.coupon.discount_percentage / 100, 2)
        else:
            return 0

    @property
    def grand_total_price(self):
        return round(self.total_price - self.coupon_discount, 2)

    def update_items_prices(self):
        if not self.is_paid:
            for item in self.items_set.all():
                item.final_price = item.product.discounted_price
                item.save()


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items_set")
    final_price = models.DecimalField(decimal_places=2, max_digits=8, editable=False)
    count = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique order product')
        ]

    def __str__(self):
        return f"{self.count}x {self.product}(s) in {self.order}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.final_price = self.product.discounted_price
        super(OrderItem, self).save(force_insert, force_update, using, update_fields)

    @property
    def total_price(self):
        return self.count * self.final_price
