from django import forms
from .models import Food, Recipe, Product, Record




ProductFormSet = forms.modelformset_factory(
    Product, fields=['have_recipe', 'weight'], extra=1
)


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories']
        labels = {
            'name': 'Food name',
            'calories': 'Food calories (per 100 gram)',
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description']
        labels = {
            'name': 'Recipe name',
            'description': 'Recipe description',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['have_recipe', 'weight']
        labels = {
            'have_recipe': 'Food',
            'weight': 'Food weight (in grams)',
        }

    # def __init__(self, *args, **kwargs):
    #     """ Overridden init to get initial product parent. """
    #     super(ProductForm, self).__init__(*args, **kwargs)

    #     # Exclude parent recipe in food Select widget
    #     initial = kwargs.get('initial', None)
    #     if initial is not None:
    #         parent_recipe = initial.get('recipe', None)
    #         if parent_recipe is not None:
    #             # Change choices excluding parent
    #             self.fields['have_recipe'].choices = [(r, str(r))
    #                                                   for r in Recipe.objects.exclude(pk=parent_recipe)]
    #         else:
    #             raise Exception("Initial parent recipe is required! (for proper form widget)")

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['recipe', 'weight']
        labels = {
            'recipe': 'Food eaten',
            'weight': 'Eaten food weight',
        }
