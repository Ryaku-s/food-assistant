from django.forms import ModelForm, IntegerField
from django.forms.models import modelformset_factory

from src.catalog.models import Food, Ingredient, Recipe, Direction


class RecipeForm(ModelForm):
    """Форма создания рецепта"""
    hours = IntegerField(label="Часы", required=False)
    minutes = IntegerField(label="Минуты")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({'class': "form-control"})
        self.fields["description"].widget.attrs.update({'class': "form-control"})
        self.fields["category"].widget.attrs.update({'class': "form-select"})
        self.fields["image"].widget.attrs.update({'class': "form-control"})
        self.fields["national_cuisine"].widget.attrs.update({'class': "form-select"})
        self.fields["hours"].widget.attrs.update({'class': "form-control"})
        self.fields["minutes"].widget.attrs.update({'class': "form-control", 'max': '59'})

    class Meta:
        model = Recipe
        exclude = ("author", "pub_date", "duration", "is_draft", "ingredients")


class DirectionForm(ModelForm):
    """Форма создания указания"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({'class': "form-control"})
        self.fields["image"].widget.attrs.update({'class': "form-control"})

    class Meta:
        model = Direction
        fields = "__all__"


DirectionFormSet = modelformset_factory(
    Direction,
    DirectionForm,
    exclude=['position', 'recipe'],
    extra=2,
    can_delete=True
)


class IngredientForm(ModelForm):
    """Форма создания ингредиента"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["food"].widget.attrs.update({'class': "form-select", 'id': "foodSelect"})
        self.fields["amount"].widget.attrs.update({'class': "form-control form-amount"})
        self.fields["unit"].widget.attrs.update({'class': "form-select form-unit"})

    class Meta:
        model = Ingredient
        exclude = "recipe",


IngredientFormSet = modelformset_factory(
    Ingredient,
    IngredientForm,
    extra=2,
    can_delete=True
)
