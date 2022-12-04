from django.urls import path

from products import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("submit-review/", views.submit_review, name="submit-review"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="single-product"),
]
