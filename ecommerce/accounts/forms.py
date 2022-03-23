from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser as User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "phone_number", "first_name", "last_name")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "...آدرس ایمیل خود را وارد کنید",
            }
        )
    )
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "...شماره موبایل خود را با فرمت ۰۹۱۲۳۴۵۶۷۸۹ وارد کنید",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام خود را وارد کنید..."}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید...",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_salesman",
        )
        widgets = {"is_salesman": forms.CheckboxInput(attrs={"class": "checkbox"})}

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["email"].label = "ایمیل"
        self.fields["phone_number"].label = "شماره موبایل"
        self.fields["first_name"].label = "نام"
        self.fields["last_name"].label = "نام خانوادگی"
        self.fields["is_salesman"].label = "فروشنده هستید؟"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs[
            "placeholder"
        ] = "رمز عبور خود را وارد کنید..."
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "رمز عبور خود را جهت تأیید مجدداً وارد کنید..."


class AccountSettingsForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    phone_number = forms.CharField(
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super(AccountSettingsForm, self).__init__(*args, **kwargs)

        self.fields["email"].label = "ایمیل"
        self.fields["phone_number"].label = "شماره موبایل"
        self.fields["first_name"].label = "نام"
        self.fields["last_name"].label = "نام خانوادگی"


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "رمز عبور قبلی خود را وارد کنید...",
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "رمز عبور جدید خود را وارد کنید...",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "placeholder": "رمز عبور جدید خود را دوباره وارد کنید...",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password1",
            "new_password2",
        )

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields["old_password"].label = "رمز عبور قبلی"
        self.fields["new_password1"].label = "رمز عبور جدید"
        self.fields["new_password2"].label = "تکرار رمز عبور جدید"


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_pic", "bio")
        widgets = {
            "profile_pic": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }
