from django.core.exceptions import ValidationError
from rest_framework import serializers

from products.models import Product, ProductCategory, ProductReview


# ProductCategory serializers

class ProductCategoryListSerializer(serializers.ModelSerializer):
    category_detail = serializers.HyperlinkedIdentityField(view_name="category-detail", lookup_field="slug")

    class Meta:
        model = ProductCategory
        exclude = ["id", "parent"]


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = ProductCategoryListSerializer()

    class Meta:
        model = ProductCategory
        exclude = ["id"]

    def get_children(self, obj: ProductCategory):
        children = obj.children_set.all()
        serializer = ProductCategoryListSerializer(children, many=True, context=self.context)

        return serializer.data


# ProductReview serializers

class ProductReviewBaseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = "__all__"

    @staticmethod
    def get_user(obj: ProductReview):
        return obj.user.username

    @staticmethod
    def get_product_id(obj: ProductReview):
        return obj.product.id

    def is_valid(self, *, raise_exception=False):
        super(ProductReviewBaseSerializer, self).is_valid(raise_exception=raise_exception)

        product_id = self.context["product_id"]
        if product_id is None:
            raise serializers.ValidationError("'product_id' is required.")
        try:
            product = Product.objects.get(id=product_id)
            self.context["product"] = product
        except (Product.DoesNotExist, ValidationError):
            if raise_exception:
                raise serializers.ValidationError(f"'{product_id}' is not a valid product id.")

    def create(self, validated_data):
        user = self.context['request'].user
        product = self.context["product"]
        content = validated_data["content"]
        return ProductReview.objects.create(user=user, product=product, content=content)


class ProductReviewListSerializer(ProductReviewBaseSerializer):
    review_detail = serializers.HyperlinkedIdentityField(view_name="review-detail")

    class Meta:
        model = ProductReview
        exclude = ["product"]

    @staticmethod
    def get_product_slug(obj: ProductReview):
        return obj.product.slug


class ProductReviewDetailSerializer(ProductReviewBaseSerializer):
    product = serializers.HyperlinkedRelatedField(view_name="product-detail", lookup_field="slug", read_only=True)


# Product serializers

class ProductBaseSerializer(serializers.ModelSerializer):
    visits_count = serializers.SerializerMethodField()
    sales_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, obj: Product):
        reviews = obj.reviews_set.all()
        serializer = ProductReviewListSerializer(reviews, many=True, context=self.context)

        return serializer.data

    @staticmethod
    def get_images(obj: Product):
        return obj.images_set.values_list("image", flat=True)

    @staticmethod
    def get_visits_count(obj: Product):
        return obj.get_visits_count()

    @staticmethod
    def get_sales_count(obj: Product):
        return obj.get_sales_count()


class ProductListSerializer(ProductBaseSerializer):
    product_detail = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field="slug")

    class Meta:
        model = Product
        exclude = ["categories"]


class ProductDetailSerializer(ProductBaseSerializer):
    categories = ProductCategoryListSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, obj: Product):
        reviews = obj.reviews_set.all()
        serializer = ProductReviewListSerializer(reviews, many=True, context=self.context)

        return serializer.data

    @staticmethod
    def get_images(obj: Product):
        return obj.images_set.values_list("image", flat=True)
