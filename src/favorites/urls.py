from django.urls import path

from src.favorites.views import FavoriteRecipeListView, AddRecipeToFavorites, RemoveRecipeFromFavorites

urlpatterns = [
    path("accounts/me/favorite-recipes/", FavoriteRecipeListView.as_view(), name="favorite_recipe_list"),
    path("recipes/<int:pk>/add-to-favorites", AddRecipeToFavorites.as_view(), name="add_recipe_to_favorites"),
    path("recipes/<int:pk>/remove-from-favorites", RemoveRecipeFromFavorites.as_view(), name="remove_recipe_from_favorites")
]
