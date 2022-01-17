from django.urls import path

from src.favorites.views import FavoriteRecipesListView, AddRecipeToFavorites, RemoveRecipeFromFavorites

urlpatterns = [
    path("catalog/favorites/", FavoriteRecipesListView.as_view(), name="favorite_recipe_list"),
    path("catalog/<int:pk>/add-to-favorites", AddRecipeToFavorites.as_view(), name="add_recipe_to_favorites"),
    path("catalog/<int:pk>/remove-from-favorites", RemoveRecipeFromFavorites.as_view(), name="remove_recipe_from_favorites")
]
