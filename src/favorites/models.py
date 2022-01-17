from django.db import models
from django.contrib.auth import get_user_model

from src.catalog.models import Recipe

User = get_user_model()


class Favorites(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="favorites", verbose_name="Пользователь")
    recipes = models.ManyToManyField(to=Recipe, verbose_name="Избранные рецепты")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"Избранное пользователя {self.user}"
