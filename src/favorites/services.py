from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect

from src.favorites.repositories import FavoritesRepository
from src.catalog.repositories import RecipeRepository


def add_recipe_to_favorites(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    favorites = FavoritesRepository.get_or_create(user=request.user)
    recipe = RecipeRepository.get_object_or_404(is_draft=False, pk=pk)
    if not recipe in favorites.recipes.all():
        favorites.recipes.add(recipe)
    return redirect(recipe)


def remove_recipe_from_favorites(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    favorites = FavoritesRepository.get_or_create(user=request.user)
    recipe = RecipeRepository.get_object_or_404(is_draft=False, pk=pk)
    if recipe in favorites.recipes.all():
        favorites.recipes.remove(recipe)
    return redirect(recipe)
