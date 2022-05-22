from django.http import JsonResponse, HttpRequest
from django.views import generic
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from src.base.mixins import AuthorRequiredMixin, RecipeFilterMixin
from src.catalog import services
from src.catalog.models import Recipe
from src.catalog.forms import RecipeForm
from src.catalog.repositories import FoodRepository, RecipeRepository, SavedRecipeRepository


class HomepageView(generic.TemplateView):
    template_name = 'catalog/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return services.get_homepage_context_data(context, self.request)


class RecipeListView(RecipeFilterMixin, generic.ListView):
    template_name = 'catalog/recipe_list.html'
    model = Recipe
    queryset = RecipeRepository.filter(is_draft=False)
    context_object_name = 'recipes'
    paginate_by = 10


class UserRecipeListView(RecipeFilterMixin, generic.ListView):
    template_name = 'catalog/user_recipe_list.html'
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 10

    def get_queryset(self):
        return RecipeRepository.filter(is_draft=False, author__id=self.kwargs['pk'])


class RecipeDetailView(generic.DetailView):
    template_name = 'catalog/recipe_detail.html'
    model = Recipe
    queryset = RecipeRepository.filter(is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return services.get_recipe_detail_context_data(
            context,
            self.request,
            self.get_object()
        )


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'catalog/recipe_form.html'
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return services.get_recipe_create_context_data(context, self.request)

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = None
        return services.RecipeFormService(request).create(self)


class RecipeUpdateView(AuthorRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return services.get_recipe_update_context_data(
            context,
            self.request,
            self.object.id
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        minutes = self.object.duration.seconds // 60
        kwargs['initial'] = {
            'hours': minutes // 60,
            'minutes': minutes % 60
        }
        return kwargs

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        return services.RecipeFormService(request).update(self, self.object)


class RecipeDeleteView(AuthorRequiredMixin, generic.DeleteView):
    model = Recipe

    def get_success_url(self) -> str:
        return reverse('homepage')


class SavedRecipeListView(LoginRequiredMixin, RecipeFilterMixin, generic.ListView):
    template_name = "catalog/favorite_recipe_list.html"
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        pks = [saved_recipe.recipe.pk for saved_recipe in SavedRecipeRepository\
            .filter(user=self.request.user)]
        print(RecipeRepository.filter(pk__in=pks))
        return RecipeRepository.filter(pk__in=pks)


@login_required
def save_recipe_to_user(request: HttpRequest, pk: int):
    return services.create_saved_recipe(request.user, pk)


@login_required
def remove_recipe_from_user(request: HttpRequest, pk: int):
    return services.delete_saved_recipe(request.user, pk)


def load_units(request: HttpRequest):
    """Загружает единицы измерения для выбранной еды (ajax)."""
    food_id = int(request.GET.get("food_id"))
    food = FoodRepository.get_object_or_none(pk=food_id)

    if not food:
        return JsonResponse({'detail': 'Food not found'}, status=404)
    units = food.units.all()

    return JsonResponse(list(units.values('id', 'name', 'is_countable')), safe=False)
