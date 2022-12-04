from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="product")
router.register(r"categories", views.ProductCategoryViewSet, basename="category")
router.register(r"reviews", views.ProductReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
