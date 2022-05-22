from src.base.repositories import ModelRepository
from src.catalog import models


class RecipeRepository(ModelRepository):
    _model = models.Recipe

    @classmethod
    def filter(cls, limit = None, *args, **kwargs):
        queryset = cls._model.objects.defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__about',
            'author__avatar',
            'author__is_staff',
            'author__is_active',
        ).filter(*args, **kwargs)
        return queryset[:limit] if limit else queryset


class CategoryRepository(ModelRepository):
    _model = models.Category


class NationalCuisineRepository(ModelRepository):
    _model = models.NationalCuisine


class DirectionRepository(ModelRepository):
    _model = models.Direction


class IngredientRepository(ModelRepository):
    _model = models.Ingredient


class FoodRepository(ModelRepository):
    _model = models.Food


class SavedRecipeRepository(ModelRepository):
    _model = models.SavedRecipe
