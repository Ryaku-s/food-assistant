from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.urls import reverse

from django_resized import ResizedImageField
from positions.fields import PositionField

from src.base.services import get_direction_image_upload_path, get_recipe_image_upload_path
from src.catalog.managers import RecipeManager, IngredientManager

User = get_user_model()


class Recipe(models.Model):
    title = models.CharField("Название рецепта", max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Автор рецепта")
    description = models.TextField("Описание рецепта", max_length=2000, blank=True)
    duration = models.DurationField("Длительность приготовления")
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE, verbose_name="Категория рецепта")
    national_cuisine = models.ForeignKey(
        to="NationalCuisine",
        on_delete=models.CASCADE,
        verbose_name="Национальная кухня"
    )
    pub_date = models.DateTimeField("Дата публикации рецепта", blank=True, null=True)
    is_draft = models.BooleanField("Черновик", default=True)
    image = ResizedImageField(
        "Изображение рецепта",
        size=[1000, 500],
        crop=['middle', 'center'],
        upload_to=get_recipe_image_upload_path,
        validators=[validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    comment = models.TextField("Примечание", max_length=2000, blank=True)

    objects = RecipeManager()

    def get_duration_display(self):
        minutes = self.duration.seconds // 60
        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
            if minutes:
                return f"{hours} ч. {minutes} мин."
            return f"{hours} ч."
        return f"{self.duration.seconds // 60} мин."

    def get_absolute_url(self):
        if self.is_draft:
            return reverse("recipe_update", kwargs={"pk": self.pk})
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-is_draft', '-pub_date']

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField("Название категории", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title


class NationalCuisine(models.Model):
    title = models.CharField("Название кухни", max_length=100)

    class Meta:
        verbose_name = "Национальная кухня"
        verbose_name_plural = "Национальные кухни"

    def __str__(self) -> str:
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name="ingredients", verbose_name="Рецепт")
    food = models.ForeignKey(to="Food", on_delete=models.CASCADE, verbose_name="Еда")
    amount = models.PositiveSmallIntegerField("Количество", blank=True, null=True)
    unit = models.ForeignKey(
        to="Unit",
        on_delete=models.CASCADE,
        related_name="count",
        verbose_name="Единица измерения"
    )

    objects = IngredientManager()

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self) -> str:
        if self.amount:
            return f"{self.food} - {self.amount} {self.unit}"
        return f"{self.food} - {self.unit}"


class Food(models.Model):
    title = models.CharField("Название еды", max_length=100)
    units = models.ManyToManyField(to="Unit", verbose_name="Допустимые единицы измерения")

    class Meta:
        verbose_name = "Еда"
        verbose_name_plural = "Еда"

    def __str__(self) -> str:
        return self.title


class Unit(models.Model):
    name = models.CharField("Обозначение единицы измерения", max_length=25)

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

    def __str__(self) -> str:
        return self.name


class Direction(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='directions', verbose_name="Рецепт")
    text = models.TextField("Текст указания к рецепту")
    image = ResizedImageField(
        "Изображение указания к рецепту",
        size=[700, 350],
        crop=['middle', 'center'],
        upload_to=get_direction_image_upload_path,
        validators=[validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    position = PositionField("Позиция", blank=True, null=True, collection='recipe')

    class Meta:
        verbose_name = "Указание к рецепту"
        verbose_name_plural = "Указания к рецепту"
        ordering = ['position']

    def __str__(self) -> str:
        return f"{self.recipe} - указание #{self.position + 1}"
