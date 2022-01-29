from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from src.catalog.models import NationalCuisine, Recipe, Category
from src.favorites.models import Favorites

User = get_user_model()


class FavoriteRecipeListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        favorites = Favorites.objects.get_or_create(user=user)[0]
        for i in range(11):
            category = Category.objects.create(title=f"Category Title {i}")
            national_cuisine = NationalCuisine.objects.create(title=f"National Cuisine Title {i}")
            recipe = Recipe.objects.create(
                title=f"Recipe Title {i}",
                author=user,
                duration=timezone.timedelta(0, 600),
                category=category,
                national_cuisine=national_cuisine,
                is_draft=False
            )
            favorites.recipes.add(recipe)

    def test_redirect_if_request_user_is_not_logged_in(self):
        response = self.client.get(reverse("favorite_recipe_list"))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse("favorite_recipe_list"))

    def test_access_permitted_if_request_user_is_logged_in(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("favorite_recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("favorite_recipe_list"))
        self.assertTemplateUsed(response, "catalog/favorite_recipe_list.html")

    def test_pagination_is_ten(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("favorite_recipe_list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 10)

    def test_pagination_next_page(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("favorite_recipe_list") + "?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 1)
