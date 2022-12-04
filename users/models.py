import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=16, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    def get_image(self):
        return "64x64.svg"


class WishlistItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items_set")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="wishlist_items_set")

    def __str__(self):
        return f"{self.product} in {self.user}'s wishlist"
