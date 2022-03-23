from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import (
    AccountSettingsForm,
    CustomPasswordChangeForm,
    EditUserProfileForm,
    SignUpForm,
)
from .models import Profile

# Create your views here.


class UserRegisterationView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class AccountSettingsView(LoginRequiredMixin, UpdateView):
    form_class = AccountSettingsForm
    template_name = "registration/account_settings.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("password_success")


def password_change_success(request):
    return render(request, "registration/password_success.html", {})


class UserProfileView(DetailView):
    model = Profile
    template_name = "accounts/profile.html"


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditUserProfileForm
    template_name = "accounts/edit_profile.html"

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        profile_slug = profile.slug
        return HttpResponseRedirect(
            reverse_lazy("profile", kwargs={"slug": profile_slug})
        )
