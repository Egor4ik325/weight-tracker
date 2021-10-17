from django.test import TestCase
from tracker.models import Recipe, Food


class RecipeManagerTests(TestCase):
    def test_manager_create_food(self):
        r = Recipe.objects.create_food(name="Apple", calories=72)
        self.assertEqual(r.name, "Apple")

        p = r.belong_recipe.first()
        f = p.have_etable
        self.assertEqual(f.name, "Apple")
        self.assertEqual(f.calories, 72)

    def test_manager_with_created_food(self):
        f = Food.objects.create(name="Apple", calories=23)
        r = Recipe.objects.create_food(name="Apple", food=f)
        self.assertEqual(r.name, "Apple")

        p = r.belong_recipe.first()
        f2 = p.have_etable
        self.assertEqual(f2.name, "Apple")
        self.assertEqual(f2.calories, 23)
