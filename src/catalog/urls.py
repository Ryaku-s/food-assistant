from django.urls import path

from src.catalog import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage"),
    path('recipes/', views.RecipeListView.as_view(), name="recipe_list"),
    path('recipes/upload', views.RecipeCreateView.as_view(), name="recipe_create"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('recipes/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipe_update"),
    path('recipes/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path('accounts/<int:pk>/recipes/', views.UserRecipeListView.as_view(), name="user_recipe_list"),
    path('accounts/me/recipes/', views.CurrentUserRecipeListView.as_view(), name="current_user_recipe_list"),

    path('ajax/load-units', views.load_units, name='ajax_load_units')
]
