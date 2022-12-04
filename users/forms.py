from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    username = forms.CharField(
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "mobile_number", "address"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ForgetPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    email = forms.EmailField(
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )


class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
