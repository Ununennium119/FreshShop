from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("activate-account/<uidb64>/<token>/", views.activate_account, name="activate-account"),
    path("forget-password/", views.ForgetPasswordView.as_view(), name="forget-password"),
    path("change-password/<uidb64>/<token>/", views.change_password, name="change-password"),

    path("account/", views.AccountView.as_view(), name="account"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
    path("reset-password/", views.reset_password, name="reset-password"),

    path("wishlist/", views.WishlistView.as_view(), name="wishlist"),
    path("remove-wishlist-item/<uuid:wishlist_item_id>/", views.remove_wishlist_item, name="remove-wishlist-item"),
    path("add-product-to-wishlist/", views.add_product_to_wishlist, name="add-product-to-wishlist"),
]
