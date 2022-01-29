from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.accounts.services import add_user_to_subscriptions, remove_user_from_subscriptions

User = get_user_model()


class SubscriptionServicesTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(email="test_follower@test.ru", password="password")
        User.objects.create_user(email="test_user@test.ru", password="password")
    
    def setUp(self) -> None:
        self.user = User.objects.get(email="test_user@test.ru")
        self.follower = User.objects.get(email="test_follower@test.ru")

    def test_follow_and_unfollow(self):
        factory = RequestFactory()
        request = factory.post(reverse("account_profile_follow", kwargs={"pk": self.user.pk}))
        request.user = self.follower
        add_user_to_subscriptions(request, self.user.pk)
        self.assertTrue(self.follower.subscriptions.filter(user=self.user).exists())
        factory = RequestFactory()
        request = factory.post(reverse("account_profile_unfollow", kwargs={"pk": self.user.pk}))
        request.user = self.follower
        remove_user_from_subscriptions(request, self.user.pk)
        self.failIf(self.follower.subscriptions.filter(user=self.user).exists())
