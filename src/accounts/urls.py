from django.urls import path

from src.accounts.views import ProfileSettingsView, ProfileSettingsUpdateView

urlpatterns = [
    path("profile/settings/", ProfileSettingsView.as_view(), name="account_profile_settings"),
    path("profile/settings/update", ProfileSettingsUpdateView.as_view(), name="account_profile_settings_update")
]
