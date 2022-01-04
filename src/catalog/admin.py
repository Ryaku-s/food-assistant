from django.contrib import admin
from src.catalog import models

admin.site.register(models.Recipe)
admin.site.register(models.Category)
admin.site.register(models.NationalCuisine)
admin.site.register(models.Direction)
admin.site.register(models.Ingredient)
admin.site.register(models.Food)
admin.site.register(models.Unit)
