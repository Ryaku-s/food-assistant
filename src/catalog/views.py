from django.urls.base import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone

from src.base.selectors import RecipeSelector, get_directions_by_recipe_id, get_ingredients_by_recipe_id
from src.catalog.services import HomepageService, get_recipes_by_fitler
from src.catalog.models import Recipe
from src.catalog.forms import IngredientFormSet, RecipeForm, DirectionFormSet
from src.base.mixins import AuthorRequiredMixin


class HomepageView(TemplateView):
    template_name = 'catalog/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(HomepageService(self.request).execute())
        return context


class RecipeListView(ListView):
    template_name = 'catalog/recipe_list.html'
    model = Recipe
    queryset = RecipeSelector.get_published_recipes()
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
    

    def get_queryset(self):
        return get_recipes_by_fitler(self.request)


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
        context['direction_formset'] = DirectionFormSet(prefix='direction', queryset=get_directions_by_recipe_id())
        context['ingredient_formset'] = IngredientFormSet(prefix='ingredient', queryset=get_ingredients_by_recipe_id())
        return context

    def post(self, request, *args, **kwargs):
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredient')
        direction_formset = DirectionFormSet(request.POST, request.FILES, prefix='direction')
        is_draft = not request.POST.get("pub")
        if recipe_form.is_valid() and ingredient_formset.is_valid() and direction_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            if request.POST.get("hours"):
                recipe.duration = timezone.timedelta(
                    hours=int(request.POST.get("hours")),
                    minutes=int(request.POST.get("minutes"))
                )
            else:
                recipe.duration = timezone.timedelta(minutes=int(request.POST.get("minutes")))
            recipe.is_draft = is_draft
            if not is_draft and not recipe.pub_date:
                recipe.pub_date = timezone.now()
            recipe.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            directions = direction_formset.save(commit=False)
            for direction in directions:
                direction.recipe = recipe
                direction.save()
            return redirect(recipe)
        else:
            return self.render_to_response(self.get_context_data(
                form=recipe_form,
                ingredient_formset=ingredient_formset,
                direction_formset=direction_formset
            ))


class RecipeUpdateView(AuthorRequiredMixin, UpdateView):
    template_name = 'catalog/recipe_form.html'
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method != 'POST':
            context['direction_formset'] = DirectionFormSet(prefix='direction', queryset=get_directions_by_recipe_id(self.get_object().id))
            context['ingredient_formset'] = IngredientFormSet(prefix='ingredient', queryset=get_ingredients_by_recipe_id(self.get_object().id))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        minutes = self.get_object().duration.seconds // 60
        kwargs['initial'] = {
            'hours': minutes // 60,
            'minutes': minutes % 60
        }
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        recipe_form = RecipeForm(request.POST, request.FILES, instance=self.get_object())
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredient')
        direction_formset = DirectionFormSet(request.POST, request.FILES, prefix='direction')
        is_draft = not request.POST.get("pub")
        if recipe_form.is_valid() and ingredient_formset.is_valid() and direction_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            if request.POST.get("hours"):
                recipe.duration = timezone.timedelta(
                    hours=int(request.POST.get("hours")),
                    minutes=int(request.POST.get("minutes"))
                )
            else:
                recipe.duration = timezone.timedelta(minutes=int(request.POST.get("minutes")))
            if not is_draft and not recipe.pub_date:
                recipe.is_draft = is_draft
                recipe.pub_date = timezone.now()
            recipe.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            directions = direction_formset.save(commit=False)
            for direction in directions:
                direction.recipe = recipe
                direction.save()
            return redirect(recipe)
        else:
            return self.render_to_response(self.get_context_data(
                form=recipe_form,
                ingredient_formset=ingredient_formset,
                direction_formset=direction_formset
            ))
