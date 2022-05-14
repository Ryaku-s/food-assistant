from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from src.catalog.models import Recipe
from src.base.mixins import RecipeFilterMixin
from src.favorites import services
from src.favorites.repositories import FavoritesRepository


class FavoriteRecipeListView(LoginRequiredMixin, RecipeFilterMixin, ListView):
    template_name = "catalog/favorite_recipe_list.html"
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return FavoritesRepository.get_or_create(user=self.request.user).recipes.all()


class AddRecipeToFavorites(View):
    def post(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponseRedirect:
        return services.add_recipe_to_favorites(request, pk)


class RemoveRecipeFromFavorites(View):
    def post(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponseRedirect:
        return services.remove_recipe_from_favorites(request, pk)
