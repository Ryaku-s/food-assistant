from django.urls.base import reverse
from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="test_views@test.ru", password="password")

    def setUp(self):
        user = User.objects.get(email="test_views@test.ru")
        self.response = self.client.get(reverse("account_profile", kwargs={"pk": user.id}))

    def test_call_view_load(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "account/profile/profile_detail.html")


class ProfileSettingsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="test_views@test.ru", password="password")

    def test_redirect_if_user_is_not_logged_in(self):
        response = self.client.get(reverse("account_profile_settings"))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse("account_profile_settings"))

    def test_access_permitted_if_request_user_is_logged_in(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("account_profile_settings"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("account_profile_settings"))
        self.assertTemplateUsed(response, "account/profile/profile_settings.html")


class ProfileSettingsUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="test_views@test.ru", password="password")

    def test_redirect_if_user_is_not_logged_in(self):
        response = self.client.get(reverse("account_profile_settings"))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse("account_profile_settings"))

    def test_access_permitted_if_request_user_is_logged_in(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("account_profile_settings_update"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("account_profile_settings_update"))
        self.assertTemplateUsed(response, "account/profile/profile_settings_form.html")
