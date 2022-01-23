from django.contrib import admin
from django.utils.html import mark_safe

from src.catalog import models


class RecipeIngredients(admin.StackedInline):
    model = models.Ingredient
    extra = 0
    
    def has_add_permission(self, request, obj) -> bool:
        return False


class RecipeDirections(admin.StackedInline):
    model = models.Direction
    extra = 0
    
    def has_add_permission(self, request, obj) -> bool:
        return False


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "image_small_display",
        "title",
        "author",
        "category",
        "duration",
        "national_cuisine",
        "pub_date",
        "is_draft"
    )
    list_filter = "category", "national_cuisine", "is_draft"
    list_display_links = "title",
    readonly_fields = "author", "pub_date", "image_small_display", "image_large_display"
    fieldsets = (
        (None, {"fields": (("title", "category"), ("national_cuisine", "duration"),)}),
        ("Публикация", {"fields": (("author", "pub_date"),)}),
        ("Изображение", {"fields": (("image", "image_large_display"),)}),
        (None, {"fields": ("comment", "is_draft")})
    )
    inlines = RecipeIngredients, RecipeDirections

    def image_small_display(self, obj):
        return mark_safe(f"<img style=\"max-width: 75px; border-radius: .25rem;\" src=\"{obj.image.url}\">")
    
    def image_large_display(self, obj):
        return mark_safe(f"<img style=\"max-width: 375px; border-radius: .25rem;\" src=\"{obj.image.url}\">")
    
    image_large_display.short_description = "Превью"


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ("food", ("amount", "unit"), "recipe")


@admin.register(models.Direction)
class DirectionAdmin(admin.ModelAdmin):
    fields = (("recipe", "position"), "text", ("image", "image_large_display"))
    readonly_fields = "image_large_display",

    def image_large_display(self, obj):
        return mark_safe(f"<img style=\"max-width: 375px; border-radius: .25rem;\" src=\"{obj.image.url}\">")
    
    image_large_display.short_description = "Превью"


admin.site.register(models.Category)
admin.site.register(models.NationalCuisine)
admin.site.register(models.Food)
admin.site.register(models.Unit)
