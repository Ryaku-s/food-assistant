from django.urls.base import reverse
from django.views.generic import View, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from src.accounts.forms import UserProfileForm
from src.accounts.services import add_user_to_subscriptions, remove_user_from_subscriptions, is_followed

User = get_user_model()


class ProfileView(DetailView):
    template_name = "account/profile/profile_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_followed"] = is_followed(self.request, self.get_object())
        return context


class AddProfileToSubscriptions(View):

    def post(self, request, pk, *args, **kwargs):
        return add_user_to_subscriptions(request, pk)


class RemoveProfileFromSubscriptions(View):

    def post(self, request, pk, *args, **kwargs):
        return remove_user_from_subscriptions(request, pk)


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
