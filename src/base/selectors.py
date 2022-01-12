from src.catalog.models import Category, Direction, Ingredient, Recipe


def get_user_subscriptions(user, limit: int = None):
    if user.is_active:
        queryset = user.subscriptions.all()
        if limit:
            return queryset[:limit]
        return queryset


def get_categories():
    return Category.objects.all()


class RecipeSelector:

    @staticmethod
    def get_published_recipes(limit: int = None):
        queryset = Recipe.objects.filter(is_draft=False)
        if limit:
            return queryset[:limit]
        return queryset

    @classmethod
    def get_recent_recipes(cls, limit: int = None):
        queryset = cls.get_published_recipes()
        if limit:
            return queryset[:limit]
        return queryset

    @staticmethod
    def get_user_recipes(user, limit: int = None):
        if user.is_active:
            queryset = Recipe.objects.filter(author=user)
            if limit:
                return queryset[:limit]
            return queryset


def get_ingredients_by_recipe_id(recipe_id: int = None):
    if recipe_id:
        return Ingredient.objects.filter(recipe_id=recipe_id)
    return Ingredient.objects.none()


def get_directions_by_recipe_id(recipe_id: int = None):
    if recipe_id:
        return Direction.objects.filter(recipe_id=recipe_id)
    return Direction.objects.none()
