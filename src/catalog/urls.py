from django.urls import path

from src.catalog.views import HomepageView, RecipeDetailView, RecipeListView, RecipeCreateView, RecipeUpdateView

urlpatterns = [
    path('', HomepageView.as_view(), name="homepage"),
    path('catalog/', RecipeListView.as_view(), name="recipe_list"),
    path('catalog/upload', RecipeCreateView.as_view(), name="recipe_create"),
    path('catalog/<int:pk>', RecipeDetailView.as_view(), name="recipe_detail"),
    path('catalog/<int:pk>/update', RecipeUpdateView.as_view(), name="recipe_update")
]
