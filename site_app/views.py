from random import shuffle

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum, OuterRef, Subquery
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from orders.models import OrderItem
from products.models import Product
from .forms import ContactForm
from .models import SliderImage, InstagramImage, SiteSetting, TeamMember


class HomePage(TemplateView):
    template_name = "site_app/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        slider_images = SliderImage.objects.filter(is_active=True)
        context["slider_images"] = slider_images

        most_viewed_products = Product.objects.filter(is_active=True) \
            .annotate(views_count=Count("visits_set")) \
            .order_by("-views_count")[:4]
        best_seller_products = Product.objects.filter(is_active=True) \
            .annotate(
            sells_count=Sum(
                Subquery(OrderItem.objects.filter(id=OuterRef("id"), order__is_paid=True).values("count"))
            )) \
            .order_by("-sells_count")[:4]

        top_products = list((most_viewed_products | best_seller_products).distinct())
        shuffle(top_products)

        context["most_viewed_products"] = most_viewed_products
        context["best_seller_products"] = best_seller_products
        context["top_products"] = top_products

        return context


class AboutPage(TemplateView):
    template_name = "site_app/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)

        members = TeamMember.objects.filter(is_active=True)
        context["members"] = members

        return context


class ContactPage(SuccessMessageMixin, CreateView):
    template_name = "site_app/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Message sent successfully!"
