from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

from src.catalog.repositories import RecipeRepository
from src.catalog.forms import IngredientFormSet, RecipeForm, DirectionFormSet


def get_homepage_context(request: HttpRequest):
    return {
        'user_recipes': RecipeRepository.filter(
            4,
            author=request.user
        ) if request.user.is_active else None,
        'recent_recipes': RecipeRepository.filter(
            2,
            is_draft=False
        ),
        'user_subscriptions': request.user.subscriptions.all()[:4]
    }


class RecipeService:

    __slots__ = 'request',

    def __init__(self, request) -> None:
        self.request = request

    def _get_recipe_form(self, instance):
        if instance:
            recipe_form = RecipeForm(self.request.POST, self.request.FILES, instance=instance)
        else:
            recipe_form = RecipeForm(self.request.POST, self.request.FILES)
        return recipe_form

    def _get_ingredient_formset(self):
        ingredient_formset = IngredientFormSet(self.request.POST, prefix='ingredient')
        return ingredient_formset

    def _get_direction_formset(self):
         direction_formset = DirectionFormSet(self.request.POST, self.request.FILES, prefix='direction')
         return direction_formset

    def _get_is_draft(self):
        return not self.request.POST.get("pub")

    def _get_duration(self):
        minutes = int(self.request.POST.get("minutes"))
        if self.request.POST.get("hours"):
            hours = int(self.request.POST.get("hours"))
            return timezone.timedelta(hours=hours, minutes=minutes)
        else:
            return timezone.timedelta(minutes=minutes)

    @staticmethod
    def _are_forms_valid(recipe_form, ingredient_formset, direction_formset):
        return recipe_form.is_valid() and ingredient_formset.is_valid() and direction_formset.is_valid()

    def _save_recipe(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.duration = self._get_duration()
        is_draft = self._get_is_draft()
        if not is_draft and not recipe.pub_date:
            recipe.is_draft = is_draft
            recipe.pub_date = timezone.now()
        recipe.save()
        return recipe

    @staticmethod
    def _save_ingredients(formset, recipe):
        ingredients = formset.save(commit=False)
        for ingredient in ingredients:
            ingredient.recipe = recipe
            ingredient.save()
        for ingredient in formset.deleted_objects:
            ingredient.delete()

    @staticmethod
    def _save_directions(formset, recipe):
        directions = formset.save(commit=False)
        for direction in directions:
            direction.recipe = recipe
            direction.save()
        for direction in formset.deleted_objects:
            direction.delete()

    def execute(self, view, instance=None):
        recipe_form = self._get_recipe_form(instance)
        ingredient_formset = self._get_ingredient_formset()
        direction_formset = self._get_direction_formset()
        if self._are_forms_valid(recipe_form, ingredient_formset, direction_formset):
            recipe = self._save_recipe(recipe_form)
            self._save_ingredients(ingredient_formset, recipe)
            self._save_directions(direction_formset, recipe)
            messages.success(self.request, f"Рецепт \"{recipe.title}\" успешно изменён")
            return redirect(recipe)
        else:
            return view.render_to_response(view.get_context_data(
                form=recipe_form,
                ingredient_formset=ingredient_formset,
                direction_formset=direction_formset
            ))
