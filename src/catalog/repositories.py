from src.base.repositories import ModelRepository
from src.catalog.models import Category, Direction, Ingredient, NationalCuisine, Recipe


class RecipeRepository(ModelRepository):
    _model = Recipe

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
    _model = Category


class NationalCuisineRepository(ModelRepository):
    _model = NationalCuisine


class DirectionRepository(ModelRepository):
    _model = Direction


class IngredientRepository(ModelRepository):
    _model = Ingredient
