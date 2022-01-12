from django.urls.base import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from src.accounts.forms import UserProfileForm

User = get_user_model()


class ProfileSettingsView(LoginRequiredMixin, DetailView):
    template_name = "account/profile/profile_settings.html"
    model = User

    def get_object(self):
        return self.request.user


class ProfileSettingsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "account/profile/profile_settings_form.html"
    model = User
    form_class = UserProfileForm

    def get_object(self):
        return self.request.user
    
    def get_success_url(self) -> str:
        return reverse("account_profile_settings")
