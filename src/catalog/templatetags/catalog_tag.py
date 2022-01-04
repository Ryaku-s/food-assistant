from django import template
from src.base.selectors import RecipeSelector

register = template.Library()


@register.inclusion_tag('catalog/tags/sidebar.html')
def get_sidebar(limit: int = None):
    recipes = RecipeSelector().get_published_recipes(limit=limit)
    return {'recipes': recipes}
