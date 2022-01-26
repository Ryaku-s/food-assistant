from django.http import JsonResponse
from django.urls.base import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from src.base.selectors import RecipeSelector, get_directions_by_recipe_id, get_ingredients_by_recipe_id
from src.catalog.services import HomepageService, RecipeService
from src.catalog.models import Food, Recipe
from src.catalog.forms import IngredientFormSet, RecipeForm, DirectionFormSet
from src.base.mixins import AuthorRequiredMixin, RecipeFilterMixin


class HomepageView(TemplateView):
    template_name = 'catalog/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(HomepageService(self.request).execute())
        return context


class RecipeListView(RecipeFilterMixin, ListView):
    template_name = 'catalog/recipe_list.html'
    model = Recipe
    queryset = RecipeSelector.get_published_recipes()
    context_object_name = 'recipes'
    paginate_by = 10


class UserRecipeListView(RecipeFilterMixin, ListView):
    template_name = 'catalog/user_recipe_list.html'
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_active:
            if self.request.user.id == self.kwargs['author_id']:
                return RecipeSelector.get_current_user_recipes(self.request)
        return RecipeSelector.get_recipes_by_author_id(self.kwargs['author_id'])


class RecipeDetailView(DetailView):
    template_name = 'catalog/recipe_detail.html'
    model = Recipe
    queryset = RecipeSelector.get_published_recipes()
    

class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'catalog/recipe_form.html'
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method != 'POST':
            context['direction_formset'] = DirectionFormSet(prefix='direction', queryset=get_directions_by_recipe_id())
            context['ingredient_formset'] = IngredientFormSet(prefix='ingredient', queryset=get_ingredients_by_recipe_id())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        return RecipeService(request).execute(self)


class RecipeUpdateView(AuthorRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method != 'POST':
            context['direction_formset'] = DirectionFormSet(
                prefix='direction',
                queryset=get_directions_by_recipe_id(self.object.id)
            )
            context['ingredient_formset'] = IngredientFormSet(
                prefix='ingredient',
                queryset=get_ingredients_by_recipe_id(self.object.id)
            )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        minutes = self.object.duration.seconds // 60
        kwargs['initial'] = {
            'hours': minutes // 60,
            'minutes': minutes % 60
        }
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return RecipeService(request).execute(self, self.object)


class RecipeDeleteView(AuthorRequiredMixin, DeleteView):
    model = Recipe

    def get_success_url(self) -> str:
        return reverse('homepage')


def load_units(request):
    """Загружает единицы измерения для выбранной еды (ajax)."""
    food_id = int(request.GET.get("food_id"))
    units = Food.objects.get(pk=food_id).units.all()
    return JsonResponse(list(units.values('id', 'name')), safe=False)
