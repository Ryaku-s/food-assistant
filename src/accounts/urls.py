from django.urls import path

from src.accounts import views

urlpatterns = [
    path("<int:pk>", views.ProfileView.as_view(), name="account_profile"),
    path("<int:pk>/follow", views.AddProfileToSubscriptions.as_view(), name="account_profile_follow"),
    path("<int:pk>/unfollow", views.RemoveProfileFromSubscriptions.as_view(), name="account_profile_unfollow"),
    path("settings/", views.ProfileSettingsView.as_view(), name="account_profile_settings"),
    path("settings/update", views.ProfileSettingsUpdateView.as_view(), name="account_profile_settings_update")
]
