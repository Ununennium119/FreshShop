import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, FormView

from products.models import Product
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ForgetPasswordForm, ChangePasswordForm
from users.models import WishlistItem, User
from users.tokens import account_activation_token, password_reset_token
from utils.mail_service import send_email


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    success_message = "Account created successfully! Activate your account via the link sent to your email."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    return redirect(request.GET.get("next", "home"))
                else:
                    messages.error(request, "Your account is not activated. Check your email!")
                    return redirect("login")
            messages.error(request, "Username or password is invalid!")

        context = {
            "form": form
        }
        return render(request, "users/login.html", context)


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User logged out successfully.")
        return redirect("login")


class ForgetPasswordView(FormView):
    template_name = "users/forget-password.html"
    form_class = ForgetPasswordForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user is not None:
                email_context = {
                    "username": user.username,
                    "domain": "127.0.0.1:8000/",
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": password_reset_token.make_token(user)
                }
                send_email("Reset Password", user.email, "email/reset-password.html", email_context)
                messages.success(request, "Password reset link sent to your email!")
                return redirect("login")
            messages.error(request, "There is no user with this email!")

        context = {
            "form": form
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class WishlistView(TemplateView):
    template_name = "users/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)

        wishlist_items = WishlistItem.objects.filter(user_id=self.request.user.id).prefetch_related("product")
        context["wishlist_items"] = wishlist_items

        return context


@method_decorator(login_required, name="dispatch")
class AccountView(TemplateView):
    template_name = "users/account.html"


@method_decorator(login_required, name="dispatch")
class EditProfileView(SuccessMessageMixin, UpdateView):
    template_name = "users/edit-profile.html"
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy("edit-profile")
    success_message = "Profile Updated!"

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.success(request, "Your account activated successfully!")
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("home")


def change_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not password_reset_token.check_token(user, token):
        messages.error(request, "Change password link is invalid!")
        return redirect("home")

    if request.method == "GET":
        form = ChangePasswordForm()
        context = {
            "form": form
        }
        return render(request, "users/change-password.html", context)
    elif request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get("password1"))
            user.save()

            if request.user.is_authenticated:
                logout(request.user)

            messages.success(request, "Password changed successfully!")
            return redirect("login")

        context = {
            "form": form
        }
        return render(request, "users/change-password.html", context)

    return redirect("home")


@login_required
def reset_password(request):
    user = User.objects.get(id=request.user.id)
    email_context = {
        "username": user.username,
        "domain": "127.0.0.1:8000/",
        "uid": urlsafe_base64_encode(force_bytes(user.id)),
        "token": password_reset_token.make_token(user)
    }
    send_email("Reset Password", user.email, "email/reset-password.html", email_context)
    messages.success(request, "Password reset link sent to your email!")

    return redirect("account")


@login_required
def remove_wishlist_item(request, wishlist_item_id):
    response = {
        "status": "failed"
    }
    content_type = "application/json"

    if request.method == "DELETE":
        try:
            wishlist_item = WishlistItem.objects.get(id=wishlist_item_id, user_id=request.user.id)
        except WishlistItem.DoesNotExist:
            return HttpResponse(json.dumps(response), content_type=content_type)

        wishlist_item.delete()
        response["status"] = "success"
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)


def add_product_to_wishlist(request):
    response = {
        "status": "failed",
        "message": "Failed to add product to wishlist!"
    }
    content_type = "application/json"

    if request.method == "POST":
        if not request.user.is_authenticated:
            response["status"] = "login"
            response["message"] = "You need to login in order to add product to wishlist."
            response["login_path"] = reverse("login")
            messages.info(request, response["message"])
            return HttpResponse(json.dumps(response), content_type=content_type)

        try:
            body = json.loads(request.body.decode("utf-8"))
            product_id = body["productId"]
            product = Product.objects.get(id=product_id, is_active=True)

        except (json.JSONDecodeError, KeyError, TypeError, Product.DoesNotExist):
            return HttpResponse(json.dumps(response), content_type=content_type)

        user = User.objects.get(id=request.user.id)
        wishlist_item, created = user.wishlist_items_set.get_or_create(product=product)

        response["status"] = "success"
        if created:
            response["message"] = "Product added to your wishlist successfully!"
        else:
            response["message"] = "Product is already in your wishlist!"
        return HttpResponse(json.dumps(response), content_type=content_type)

    return HttpResponse(json.dumps(response), content_type=content_type)
