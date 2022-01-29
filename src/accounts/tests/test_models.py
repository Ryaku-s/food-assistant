from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="test_recipe_model@test.ru",
            password="password"
        )
    
    def setUp(self):
        self.user = User.objects.get(email="test_recipe_model@test.ru")

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/accounts/1/")

    def test_str(self):
        self.assertEqual(str(self.user), "test_recipe_model@test.ru")
    
    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "test_recipe_model@test.ru")
    
    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "test_recipe_model@test.ru")
        self.user.display_name = "User Display Name"
        self.assertEqual(self.user.get_short_name(), "User Display Name")
