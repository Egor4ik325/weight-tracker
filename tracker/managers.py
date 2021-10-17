from django.db import models
import tracker.models as tracker_models


def get_model_field_names(model):
    return [field.name for field in model._meta.get_fields()]


def filter_field_kwargs(model, kwargs):
    return dict(
        filter(lambda kwarg: kwarg[0] in get_model_field_names(model), kwargs.items())
    )


class RecipeManager(models.Manager):
    def create_food(self, **kwargs):
        recipe_kwargs = filter_field_kwargs(tracker_models.Recipe, kwargs)
        recipe = self.create(**recipe_kwargs)

        # Create food if not passed
        food = kwargs.get("food")
        if food is None:
            food_kwargs = filter_field_kwargs(tracker_models.Food, kwargs)
            food = tracker_models.Food.objects.create(**food_kwargs)

        product = tracker_models.Product.objects.create(recipe=recipe, have_food=food)
        return recipe
