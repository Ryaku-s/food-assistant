from django import template
from src.catalog.repositories import RecipeRepository

register = template.Library()


@register.inclusion_tag('catalog/tags/sidebar.html')
def get_sidebar(limit: int = 5):
    return {
        'recipes': RecipeRepository.filter(
            limit,
            is_draft=False
        ),
    }
