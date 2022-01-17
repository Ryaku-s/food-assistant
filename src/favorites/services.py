from django.shortcuts import redirect

from src.base.selectors import RecipeSelector, get_or_create_favorites


def add_recipe_to_favorites(request, pk):
    favorites = get_or_create_favorites(request.user)
    recipe = RecipeSelector.get_published_recipes().get(pk=pk)
    if not recipe in favorites.recipes.all():
        favorites.recipes.add(recipe)
    return redirect(recipe)


def remove_recipe_from_favorites(request, pk):
    favorites = get_or_create_favorites(request.user)
    recipe = RecipeSelector.get_published_recipes().get(pk=pk)
    if recipe in favorites.recipes.all():
        favorites.recipes.remove(recipe)
    return redirect(recipe)
