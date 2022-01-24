from django.contrib.auth import get_user_model

from src.catalog.models import Category, Direction, Ingredient, Recipe
from src.favorites.models import Favorites
from src.accounts.models import Follower

User = get_user_model()


def get_user_by_pk(pk: int):
    return User.objects.get(pk=pk)


def get_user_subscriptions(user, limit: int = None):
    if user.is_active:
        queryset = user.subscriptions.all()
        if limit:
            return queryset[:limit]
        return queryset


def get_or_create_follower(user, subscriber):
    return Follower.objects.get_or_create(user=user, subscriber=subscriber)[0]


def get_or_create_favorites(user):
    return Favorites.objects.get_or_create(user=user)[0]


def get_categories():
    return Category.objects.all()


class RecipeSelector:

    @staticmethod
    def get_published_recipes(limit: int = None):
        queryset = Recipe.objects.filter(is_draft=False)
        if limit:
            return queryset[:limit]
        return queryset

    @classmethod
    def get_recent_recipes(cls, limit: int = None):
        queryset = cls.get_published_recipes()
        if limit:
            return queryset[:limit]
        return queryset

    @staticmethod
    def get_recipes_by_author_id(author_id, limit: int = None):
        author = get_user_by_pk(author_id)
        if author.is_active:
            queryset = Recipe.objects.filter(author__id=author_id)
            if limit:
                return queryset[:limit]
            return queryset

    @staticmethod
    def get_favorite_recipes_by_user(user, limit: int = None):
        favorites = get_or_create_favorites(user)
        queryset = favorites.recipes.all()
        if limit:
            return queryset[:limit]
        return queryset


def get_ingredients_by_recipe_id(recipe_id: int = None):
    if recipe_id:
        return Ingredient.objects.filter(recipe_id=recipe_id)
    return Ingredient.objects.none()


def get_directions_by_recipe_id(recipe_id: int = None):
    if recipe_id:
        return Direction.objects.filter(recipe_id=recipe_id)
    return Direction.objects.none()
