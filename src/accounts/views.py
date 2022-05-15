from django.urls.base import reverse
from django.views.generic import View, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from src.accounts import services
from src.accounts.models import Follower
from src.accounts.forms import UserProfileForm

User = get_user_model()


class SubscriptionListView(ListView):
    template_name = "account/profile/profile_list.html"
    models = Follower
    context_object_name = "subscriptions"
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_active:
            return self.request.user.subscriptions.all()


class ProfileDetailView(DetailView):
    template_name = "account/profile/profile_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return services.get_profile_detail_context_data(context, self.request, self.object)


class AddProfileToSubscriptions(View):

    def post(self, request, pk, *args, **kwargs):
        return services.add_user_to_subscriptions(request, pk)


class RemoveProfileFromSubscriptions(View):

    def post(self, request, pk, *args, **kwargs):
        return services.remove_user_from_subscriptions(request, pk)


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
