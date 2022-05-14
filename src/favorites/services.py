from django.shortcuts import redirect

from src.base.repositories import get_or_create_favorites
from src.catalog.repositories import RecipeRepository


def add_recipe_to_favorites(request, pk):
    favorites = get_or_create_favorites(request.user)
    recipe = RecipeRepository.filter(is_draft=False, pk=pk)
    if not recipe in favorites.recipes.all():
        favorites.recipes.add(recipe)
    return redirect(recipe)


def remove_recipe_from_favorites(request, pk):
    favorites = get_or_create_favorites(request.user)
    recipe = RecipeRepository.filter(is_draft=False, pk=pk)
    if recipe in favorites.recipes.all():
        favorites.recipes.remove(recipe)
    return redirect(recipe)
