from django.apps import AppConfig


class FavoritesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.favorites'
    verbose_name = "Избранное"
