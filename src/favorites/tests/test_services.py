from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone

from src.favorites.services import add_recipe_to_favorites, remove_recipe_from_favorites
from src.catalog.models import NationalCuisine, Recipe, Category
from src.favorites.models import Favorites

User = get_user_model()


class TestAddRecipeToFavorites(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        Favorites.objects.create(user=user)
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=False
        )
    
    def setUp(self) -> None:
        self.user = User.objects.get(email="test_views@test.ru")
        self.recipe = Recipe.objects.get(title="Recipe Title")
    
    def test_add_recipe_to_favorites(self):
        request = RequestFactory()
        request.user = self.user
        add_recipe_to_favorites(request, self.recipe.id)
        self.assertTrue(self.user.favorites.recipes.filter(title="Recipe Title").exists())
    
    def test_add_duplicates_in_favorites(self):
        request = RequestFactory()
        request.user = self.user
        for i in range(5):
            add_recipe_to_favorites(request, self.recipe.id)
        self.failIf(len(self.user.favorites.recipes.all()) > 1)


class TestRemoveRecipeFromFavorites(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        favorites = Favorites.objects.create(user=user)
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        recipe = Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=False
        )
        favorites.recipes.add(recipe)
    
    def setUp(self) -> None:
        self.user = User.objects.get(email="test_views@test.ru")
        self.recipe = Recipe.objects.get(title="Recipe Title")
    
    def test_remove_recipe_from_favorites(self):
        request = RequestFactory()
        request.user = self.user
        remove_recipe_from_favorites(request, self.recipe.id)
        self.failIf(self.user.favorites.recipes.filter(title="Recipe Title").exists())
