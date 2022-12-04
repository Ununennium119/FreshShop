from django.contrib import admin
from .models import Product, ProductImage, ProductCategory, ProductVisit, ProductReview


class PictureInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "discount_percentage", "discounted_price", "available_quantity", "is_active"]
    list_editable = ["price", "discount_percentage", "available_quantity", "is_active"]
    list_filter = ["is_active"]
    readonly_fields = ["slug"]
    inlines = [PictureInline]


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "slug", "is_active"]
    list_editable = ["parent", "is_active"]
    list_filter = ["is_active"]
    readonly_fields = ["slug"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductVisit)
admin.site.register(ProductReview)
