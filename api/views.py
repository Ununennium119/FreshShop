from rest_framework import permissions
from rest_framework import viewsets, mixins

from products.models import Product, ProductCategory, ProductReview
from . import serializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductBaseSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductDetailSerializer
        else:
            return serializers.ProductListSerializer


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.ProductCategoryDetailSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductCategoryDetailSerializer
        else:
            return serializers.ProductCategoryListSerializer


class ProductReviewViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = serializers.ProductReviewListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductReviewDetailSerializer
        else:
            return serializers.ProductReviewListSerializer
    
    def get_serializer_context(self):
        context = super(ProductReviewViewSet, self).get_serializer_context()
        context["product_id"] = self.request.POST.get("product_id")
        return context
