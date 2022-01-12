from django.urls import path

from src.catalog import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage"),
    path('catalog/', views.RecipeListView.as_view(), name="recipe_list"),
    path('catalog/my/', views.UserRecipeListView.as_view(), name="user_recipe_list"),
    path('catalog/upload', views.RecipeCreateView.as_view(), name="recipe_create"),
    path('catalog/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
    path('catalog/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipe_update"),
    path('catalog/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipe_delete")
]
