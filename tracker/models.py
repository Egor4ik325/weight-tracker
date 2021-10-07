from django.db import models

# context string internationalization support
from django.utils.translation import ugettext_lazy as _

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

    def __str__(self):
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
    have_food = models.ForeignKey(Food, on_delete=models.RESTRICT, null=True, blank=True)

    # can't specify all recipe choices without recipe parent
    have_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True, related_name='have_recipe') # parent_recipes
    weight = models.FloatField(default=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='belong_recipe') # child_recipes

    def __str__(self):
        if self.have_food is None:
            if self.have_recipe is None:
                # shouldn't be but could
                return None
            else:
                return str(self.have_recipe)
        else:
            return str(self.have_food)

    @property
    def total(self):
        """ Total product calorie value. """
        if self.have_food is None:
            if self.have_recipe is None:
                # Product object is not bound to any food/recipe object
                # shouldn't be but could
                return None
            else:
                return (self.weight * self.have_recipe.calories) / 100
        else:
            return (self.weight * self.have_food.calories) / 100

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
