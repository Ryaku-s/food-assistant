from django.db.models import Manager


class RecipeManager(Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'category',
            'national_cuisine',
            'author'
        )


class IngredientManager(Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('recipe', 'food', 'unit')
