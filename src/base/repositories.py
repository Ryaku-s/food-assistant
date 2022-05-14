from typing import Optional, Type

from django.db.models import Model, QuerySet
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from src.catalog.models import Category, Direction, Ingredient, Recipe
from src.favorites.models import Favorites
from src.accounts.models import Follower

User = get_user_model()


class ModelRepository:
    model: Type[Model]

    @classmethod
    def all(cls, limit: Optional[int] = None) -> QuerySet:
        queryset = cls.model.objects.all()
        return queryset[:limit] if limit else queryset

    @classmethod
    def filter(cls, limit: Optional[int] = None, *args, **kwargs) -> QuerySet:
        queryset = cls.model.objects.filter(*args, **kwargs)
        return queryset[:limit] if limit else queryset

    @classmethod
    def get(cls, *args, **kwargs) -> Model:
        return cls.model.objects.get(*args, **kwargs)

    @classmethod
    def get_object_or_404(cls, *args, **kwargs) -> Model:
        return get_object_or_404(cls.model, *args, **kwargs)

    @classmethod
    def get_or_create(cls, **kwargs) -> Model:
        return cls.model.objects.get_or_create(**kwargs)[0]

    @classmethod
    def none(cls):
        return cls.model.objects.none()


def get_user_by_pk(pk: int):
    return get_object_or_404(User, pk=pk)


def get_user_subscriptions(user, limit: int = None):
    if user.is_active:
        queryset = user.subscriptions.all()
        if limit:
            return queryset[:limit]
        return queryset


def get_or_create_follower(user, subscriber):
    if user != subscriber:
        return Follower.objects.get_or_create(user=user, subscriber=subscriber)[0]


def get_or_create_favorites(user):
    return Favorites.objects.get_or_create(user=user)[0]


def get_categories():
    return Category.objects.all()


class RecipeSelector:

    @staticmethod
    def get_published_recipes(limit: int = None):
        queryset = Recipe.objects.filter(is_draft=False, author__is_active=True)
        if limit:
            return queryset[:limit]
        return queryset

    @classmethod
    def get_recipes_by_author_id(cls, author_id, limit: int = None):
        author = get_user_by_pk(author_id)
        if author.is_active:
            queryset = cls.get_published_recipes().filter(author__id=author_id)
            if limit:
                return queryset[:limit]
            return queryset
    
    @staticmethod
    def get_current_user_recipes(request, limit: int = None):
        user = request.user
        if user.is_active:
            queryset = Recipe.objects.filter(author__id=user.id)
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
