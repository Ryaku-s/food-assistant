from typing import Any, Dict, Type, Union

from django.utils import timezone
from django import http
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import BaseModelFormSet
from django.views.generic import CreateView, UpdateView

from src.base.services import build_context_data
from src.catalog.forms import IngredientFormSet, DirectionFormSet, RecipeForm
from src.catalog.models import Recipe
from src.catalog.repositories import DirectionRepository, IngredientRepository, RecipeRepository


def get_homepage_context_data(
    base_context: Dict[str, Any],
    request: http.HttpRequest
) -> Dict[str, Any]:
    return build_context_data(
        base_context,
        user_recipes=RecipeRepository.filter(4, author=request.user)
            if request.user.is_active else None,
        recent_recipes=RecipeRepository.filter(2, is_draft=False),
        user_subscriptions=request.user.subscriptions.all()[:4]
            if request.user.is_active else None
    )


def get_recipe_create_context_data(
    base_context: Dict[str, Any],
    request: http.HttpRequest
) -> Dict[str, Any]:
    if request.method != 'POST':
        return build_context_data(
            base_context,
            direction_formset=DirectionFormSet(
                prefix='direction',
                queryset=DirectionRepository.none()
            ),
            ingredient_formset=IngredientFormSet(
                prefix='ingredient',
                queryset=IngredientRepository.none()
            )
        )
    return base_context


def get_recipe_update_context_data(
    base_context: Dict[str, Any],
    request: http.HttpRequest,
    pk: int
) -> Dict[str, Any]:
    if request.method != 'POST':
        return build_context_data(
            base_context,
            direction_formset=DirectionFormSet(
                prefix='direction',
                queryset=DirectionRepository.filter(recipe__pk=pk)
            ),
            ingredient_formset=IngredientFormSet(
                prefix='ingredient',
                queryset=IngredientRepository.filter(recipe__pk=pk)
            )
        )
    return base_context


class RecipeFormService:

    __slots__ = '__request',

    def __init__(self, request: http.HttpRequest) -> None:
        self.__request = request

    def create(self, view: Type[CreateView]):
        recipe_form = self.__get_recipe_create_form()
        return self.__save(view, recipe_form)

    def update(self, view: Type[CreateView], instance: Recipe):
        recipe_form = self.__get_recipe_update_form(instance)
        return self.__save(view, recipe_form)

    def __get_recipe_create_form(self) -> RecipeForm:
        return RecipeForm(self.__request.POST, self.__request.FILES)

    def __get_recipe_update_form(self, instance: Recipe) -> RecipeForm:
        return RecipeForm(
            self.__request.POST,
            self.__request.FILES,
            instance=instance
        )

    def __get_ingredient_formset(self):
        return IngredientFormSet(
            self.__request.POST,
            prefix='ingredient'
        )

    def __get_direction_formset(self):
        return DirectionFormSet(
            self.__request.POST,
            self.__request.FILES,
            prefix='direction'
        )

    def __get_is_draft(self):
        return not self.__request.POST.get("pub")

    def __get_duration(self):
        minutes = int(self.__request.POST.get("minutes"))
        if self.__request.POST.get("hours"):
            hours = int(self.__request.POST.get("hours"))
            return timezone.timedelta(hours=hours, minutes=minutes)
        return timezone.timedelta(minutes=minutes)

    def __get_author(self):
        return self.__request.user

    def __are_forms_valid(self, *forms) -> bool:
        for form in forms:
            if not form.is_valid():
                return False
        return True

    def __save_recipe(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.__get_author()
        recipe.duration = self.__get_duration()
        is_draft = self.__get_is_draft()
        if not is_draft and not recipe.pub_date:
            recipe.is_draft = is_draft
            recipe.pub_date = timezone.now()
        recipe.save()
        return recipe

    def __save_formset(self, formset: BaseModelFormSet, recipe: Recipe):
        objects = formset.save(commit=False)
        for obj in objects:
            obj.recipe = recipe
            obj.save()
        for obj in formset.deleted_objects:
            obj.delete()

    def __save_ingredients(self, ingredient_formset: IngredientFormSet, recipe: Recipe):
        self.__save_formset(ingredient_formset, recipe)

    def __save_directions(self, direction_formset: DirectionFormSet, recipe: Recipe):
        self.__save_formset(direction_formset, recipe)

    def __save(self, view: Union[Type[CreateView], Type[UpdateView]], recipe_form: RecipeForm) -> Union[http.HttpResponseRedirect, http.HttpResponse]:
        ingredient_formset = self.__get_ingredient_formset()
        direction_formset = self.__get_direction_formset()
        if self.__are_forms_valid(recipe_form, ingredient_formset, direction_formset):
            recipe = self.__save_recipe(recipe_form)

            self.__save_ingredients(ingredient_formset, recipe)
            self.__save_directions(direction_formset, recipe)

            messages.success(self.__request, f"Рецепт \"{recipe.title}\" успешно изменён")
            return redirect(recipe)
        else:
            return view.render_to_response(view.get_context_data(
                form=recipe_form,
                ingredient_formset=ingredient_formset,
                direction_formset=direction_formset
            ))
