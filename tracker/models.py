from django.db import models

# context string internationalization support
from django.utils.translation import ugettext_lazy as _

from .managers import RecipeManager

# Relations:
# ForeignKey - M-to-1
# 

# on_delete = What to do with the objects referencing deleting object
# - also delete (CASCADE)
# - restrict deletion (RESTRICT)
# - set reference to NULL (SET NULL)

# blank - can be skipped by the user
# null - can be actually stored in database as NULL not '' or 0
# default - value by default (with blank and null)

# related_name is used to name relation (for use: Parent.<related_name>.all(), child_set)

class Food(models.Model):
    """ General class representing food, used in eaten food records. """
    name = models.CharField(max_length=100, unique=True)
    # calories per 100 gram
    calories = models.FloatField(verbose_name=_("Food calories in 100 gram"))

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Food")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """ Recipe - collection of food. Complex & distinct.
    Can consist of one or multiple products. """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    objects = RecipeManager()

    def is_food_alias(self):
        """Determine whether recipe is food/recipe alias."""
        return self.belong_recipe.count() == 1

    def __str__(self):
        if self.is_food_alias():
            return str(self.belong_recipe.first().have_etable)

        return self.name

    @property
    def calories(self):
        """ Recipe calories per 100 gram. """
        product_totals = sum([p.total for p in self.belong_recipe.all()])
        product_weights = sum([p.weight for p in self.belong_recipe.all()])
        if product_weights == 0:
            return None
        else:
            return (product_totals / product_weights) * 100

class Product(models.Model):
    """ Some real food (have weight) that is bind to simple/complex
    (from one or multiple products) recipe. """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='belong_recipe') # child_recipes

    # can't specify all recipe choices without recipe parent
    have_food = models.ForeignKey(Food, on_delete=models.RESTRICT, null=True, blank=True)
    have_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True, related_name='have_recipe') # parent_recipes
    weight = models.FloatField(default=100)

    @property
    def have_etable(self):
        """Return Food or Recipe object that product is pointing to."""
        if self.have_food is not None:
            return self.have_food
        
        if self.have_recipe is not None:
            return self.have_recipe

        # Shouldn't happen
        raise

    def __str__(self):
        return f"{self.recipe} - {self.have_etable}"

    @property
    def total(self):
        """Total product calorie value."""
        return (self.weight * self.have_etable.calories) / 100

class Record(models.Model):
    """ Represent eaten food record at some day and day section (zone). """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Eaten food")
    # weight choices for ModelForm for form Select widget
    WEIGHT_CHOICES = [
        (10, 10),
        (100, 100),
        (150, 150),
        (200, 200),
        (250, 250),
    ]
    weight = models.FloatField(choices=WEIGHT_CHOICES, verbose_name="Weight of eaten food")
    date_added = models.DateField(auto_now_add=True)
    section = models.IntegerField()

    @property
    def total(self):
        """ Total eaten food calories. """
        return self.weight * self.recipe.calories

    def __str__(self):
        return str(self.recipe)
