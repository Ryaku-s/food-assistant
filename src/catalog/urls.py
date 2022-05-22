from django.urls import path

from src.catalog import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage"),
    path('recipes/', views.RecipeListView.as_view(), name="recipe_list"),
    path('recipes/upload', views.RecipeCreateView.as_view(), name="recipe_create"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('recipes/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipe_update"),
    path('recipes/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path("recipes/<int:pk>/save-in-favorites", views.save_recipe_to_user, name="save_recipe_in_favorites"),
    path("recipes/<int:pk>/remove-from-favorites", views.remove_recipe_from_user, name="remove_recipe_from_favorites"),

    path('accounts/<int:pk>/recipes/', views.UserRecipeListView.as_view(), name="user_recipe_list"),
    path("accounts/<int:pk>/favorite-recipes/", views.SavedRecipeListView.as_view(), name="favorite_recipe_list"),

    path('ajax/load-units', views.load_units, name='ajax_load_units')
]
