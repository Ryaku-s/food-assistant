from src.base.repositories import ModelRepository
from src.catalog.models import Direction, Ingredient, Recipe


class RecipeRepository(ModelRepository):
    model = Recipe

    @classmethod
    def filter(cls, limit = None, *args, **kwargs):
        queryset = cls.model.objects.defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__about',
            'author__avatar',
            'author__is_staff',
            'author__is_active',
        ).filter(*args, **kwargs)
        return queryset[:limit] if limit else queryset


class DirectionRepository(ModelRepository):
    model = Direction


class IngredientRepository(ModelRepository):
    model = Ingredient
