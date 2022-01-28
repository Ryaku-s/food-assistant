from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from src.catalog.models import NationalCuisine, Recipe, Category, Ingredient, Food, Unit

User = get_user_model()


class TestRecipeModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email="test_recipe_model@test.ru",
            password="password"
        )
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=True
        )

    def setUp(self):
        self.recipe = Recipe.objects.get(title="Recipe Title")
    
    def test_get_duration_display(self):
        self.assertEqual(self.recipe.get_duration_display(), "10 мин.")
        self.recipe.duration = timezone.timedelta(0, 3600)
        self.assertEqual(self.recipe.get_duration_display(), "1 ч.")
        self.recipe.duration = timezone.timedelta(0, 4200)
        self.assertEqual(self.recipe.get_duration_display(), "1 ч. 10 мин.")

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), "/catalog/1/update")
        self.recipe.is_draft = False
        self.assertEqual(self.recipe.get_absolute_url(), "/catalog/1/")
    
    def test_str(self):
        self.assertEqual(str(self.recipe), "Recipe Title")
    
    def tearDown(self):
        User.objects.get(email="test_recipe_model@test.ru").delete()
        Category.objects.get(title="Category Title").delete()
        NationalCuisine.objects.get(title="National Cuisine Title").delete()


class TestIngredientModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email="test_recipe_model@test.ru",
            password="password"
        )
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        recipe = Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=True
        )
        unit = Unit.objects.create(name="Unit Name")
        food = Food.objects.create(title="Food Title")
        food.units.add(unit)
        Ingredient.objects.create(recipe=recipe, food=food, amount=15, unit=unit)
    
    def setUp(self):
        self.ingredient = Ingredient.objects.get(pk=1)
    
    def test_str(self):
        self.assertEqual(str(self.ingredient), "Food Title - 15 Unit Name")
        self.ingredient.amount = 0
        self.assertEqual(str(self.ingredient), "Food Title - Unit Name")
    
    def tearDown(self):
        User.objects.get(email="test_recipe_model@test.ru").delete()
        Category.objects.get(title="Category Title").delete()
        NationalCuisine.objects.get(title="National Cuisine Title").delete()
        Food.objects.get(title="Food Title").delete()
        Unit.objects.get(name="Unit Name").delete()
        self.ingredient.delete()
