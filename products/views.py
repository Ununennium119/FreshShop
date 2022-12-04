import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from products.models import Product, ProductCategory, ProductVisit
from users.models import User


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/single-product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product: Product = self.object

        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                user = User.objects.get(id=user_id)
                ProductVisit.objects.get_or_create(user=user, product=product)
            except User.DoesNotExist:
                pass

        product_images = [image_obj.image for image_obj in list(product.images_set.all())]
        product_images.insert(0, product.get_main_image())
        context["product_images"] = product_images
        context["images_count"] = len(product_images)

        featured_products = Product.objects.filter(is_active=True) \
            .annotate(visits_count=Count("visits_set")) \
            .order_by("-visits_count")[:7]
        context["featured_products"] = featured_products

        return context


class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 9

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()

        category_slug = self.request.GET.get("category")
        if category_slug:
            query = query.filter(categories__slug=category_slug)

        search_query = self.request.GET.get("search_query")
        start_price = self.request.GET.get("start_price")
        end_price = self.request.GET.get("end_price")
        if search_query is None:
            search_query = ""
        if start_price is None:
            start_price = 0
        if end_price is None:
            end_price = Product.MAX_PRICE
        query = query.filter(Q(name__icontains=search_query) |
                             Q(description__icontains=search_query),
                             is_active=True,
                             discounted_price__range=(start_price, end_price)) \
            .annotate(visits_count=Count("visits_set")).prefetch_related("images_set")

        sort_key = self.request.GET.get("sort")
        match sort_key:
            case "sell":
                pass
            case "price-desc":
                query = query.order_by("-discounted_price")
            case "price-asc":
                query = query.order_by("discounted_price")
            case _:
                query = query.order_by("-visits_count")

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        request = self.request

        sort_key = request.GET.get("sort")
        context["sort"] = sort_key if sort_key else "popular"

        search_query = request.GET.get("search_query")
        context["search_query"] = search_query if search_query else ""

        category_slug = request.GET.get("category")
        context["category_slug"] = category_slug if category_slug else ""

        start_price = request.GET.get("start_price")
        context["start_price"] = start_price if start_price is not None else 0

        end_price = request.GET.get("end_price")
        context["end_price"] = end_price if end_price is not None else Product.MAX_PRICE

        return context


def product_category_component(request):
    categories = ProductCategory.objects.filter(is_active=True).prefetch_related("children_set", "parent")

    selected_category_slug = request.GET.get("category", )
    try:
        selected_category = ProductCategory.objects.get(slug=selected_category_slug)
    except ProductCategory.DoesNotExist:
        selected_category = None
    selected_category_parent = selected_category.parent if selected_category else None

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "selected_category_parent": selected_category_parent
    }
    return render(request, "products/components/category_component.html", context)


@login_required
def submit_review(request):
    response = {
        "status": "failed",
        "message": "Failed to submit review!"
    }
    content_type = "application/json"

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            product_id = body["productId"]
            review_content = body["review"]
            product = Product.objects.get(id=product_id, is_active=True)

        except (json.JSONDecodeError, KeyError, TypeError, Product.DoesNotExist):
            return HttpResponse(json.dumps(response), content_type=content_type)

        if len(review_content) < 4:
            response["message"] = "Review should at least contain 4 characters!"
            return HttpResponse(json.dumps(response), content_type=content_type)

        user = User.objects.get(id=request.user.id)
        review = product.reviews_set.create(user_id=user.id, content=review_content)

        review_dict = {
            "username": user.username,
            "image": user.get_image(),
            "content": review.content,
            "create_time": review.create_time.strftime("%Y-%m-%d, %I:%M %p")
        }

        response["status"] = "success"
        response["message"] = "Review Submitted!"
        response["review"] = review_dict
        response["user_image"] = user.get_image()
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)