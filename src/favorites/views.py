from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from src.catalog.models import Recipe
from src.base.repositories import RecipeSelector
from src.base.mixins import RecipeFilterMixin
from src.favorites import services


class FavoriteRecipeListView(LoginRequiredMixin, RecipeFilterMixin, ListView):
    template_name = "catalog/favorite_recipe_list.html"
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return RecipeSelector.get_favorite_recipes_by_user(self.request.user)


class AddRecipeToFavorites(View):
    def post(self, request, pk, *args, **kwargs):
        return services.add_recipe_to_favorites(request, pk)


class RemoveRecipeFromFavorites(View):
    def post(self, request, pk, *args, **kwargs):
        return services.remove_recipe_from_favorites(request, pk)
