import uuid

from autoslug import AutoSlugField
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class ProductCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=64)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children_set")
    slug = AutoSlugField(max_length=128, unique=True, db_index=True, populate_from="name")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "product categories"

    def __str__(self):
        return str(self.name)

    def contains_category(self, category_id):
        return self.id == category_id or self.children_set.filter(id=category_id).exists()


class Product(models.Model):
    MAX_PRICE = 9999

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    discount_percentage = models.IntegerField(default=0)
    discounted_price = models.DecimalField(default=price, decimal_places=2, max_digits=6, editable=False)
    available_quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField(ProductCategory, related_name="related_products_set")
    main_image = models.ImageField(upload_to="product-images", null=True, blank=True)
    slug = AutoSlugField(max_length=128, unique=True, db_index=True, populate_from="name")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.discounted_price = self.price * (100 - self.discount_percentage) / 100
        super(Product, self).save(force_insert, force_update, using, update_fields)

    def get_visits_count(self) -> int:
        return ProductVisit.objects.filter(product_id=self.id).count()

    def get_sales_count(self) -> int:
        return self.order_items_set.aggregate(count__sum=Coalesce(Sum("count"), 0))["count__sum"]

    def get_main_image(self):
        if self.main_image:
            return self.main_image
        else:
            return "product-images/product-default.jpg"

    def get_absolute_url(self):
        return reverse("single-product", args=[self.slug])


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images_set")
    image = models.ImageField(upload_to="product-images")

    def __str__(self):
        return str(self.image.name)


class ProductVisit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="visits_set")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="visits_set")

    def __str__(self):
        return f"{self.product} visited by {self.user}"


class ProductReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews_set")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews_set")
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()

    class Meta:
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.user}'s review on {self.product}"
