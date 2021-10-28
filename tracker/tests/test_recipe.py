from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from tracker.models import Recipe, Product


class RecipeTemplateTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_create_recipe(self):
        # Create test food
        apple = Recipe.objects.create_food(name="Apple", calories=72)
        sugar = Recipe.objects.create_food(name="Sugar", calories=120)
        flour = Recipe.objects.create_food(name="Flour", calories=23)
        recipe_name = "Apple Pie"
        recipe_description = "Apple pie recipe from apples, sugar and flour!"

        url = self.live_server_url + reverse("tracker:add_recipe")
        self.driver.get(url)

        # Recipe form
        name, description, submit = self._get_recipe_form_controls()
        self.assertEqual(self._get_total_forms(), 1)
        name.send_keys(recipe_name)
        description.send_keys(recipe_description)

        product_form_0 = self._get_product_form(0)
        recipe_select = Select(product_form_0["have_recipe"])
        recipe_select.select_by_value(str(apple.id))
        product_form_0["weight"].clear()
        product_form_0["weight"].send_keys(500)

        self._add_product(sugar.id, 50)
        self._add_product(flour.id, 150)

        submit.click()
        recipe = Recipe.objects.last()
        self.assertEqual(recipe.name, recipe_name)
        self.assertEqual(recipe.description, recipe_description)
        products = recipe.belong_recipe
        self.assertEqual(products.count(), 3)
        products.get(have_recipe=apple)
        products.get(have_recipe=sugar)
        products.get(have_recipe=flour)

    def test_recipe_update(self):
        """Assert editing recipe (complex food) is in fact working."""
        # What is its calories
        apple = Recipe.objects.create_food(name="Apple", calories=72)
        sugar = Recipe.objects.create_food(name="Sugar", calories=120)
        flour = Recipe.objects.create_food(name="Flour", calories=23)
        salt = Recipe.objects.create_food(name="Salt", calories=34)
        # What in where?
        apple_pie = Recipe.objects.create(
            name="Apple Pie",
            description="Apple pie recipe from apples, sugar and flour!",
        )
        # How much of what?
        apple_product = Product.objects.create(
            weight=500, recipe=apple_pie, have_recipe=apple
        )
        sugar_product = Product.objects.create(
            weight=50, recipe=apple_pie, have_recipe=sugar
        )
        flour_product = Product.objects.create(
            weight=150, recipe=apple_pie, have_recipe=flour
        )

        self.driver.get(
            self.live_server_url
            + reverse("tracker:edit_food", kwargs={"food_id": apple_pie.id})
        )
        name, description, submit = self._get_recipe_form_controls()
        self.assertEqual(self._get_total_forms_update(), 3)
        # Update recipe
        name.send_keys("2")
        description.send_keys("2")

        # Update recipe food
        apple_form = self._get_product_form_update(0)
        apple_form["weight"].clear()
        apple_form["weight"].send_keys(700)
        sugar_form = self._get_product_form_update(1)
        Select(sugar_form["have_recipe"]).select_by_value(str(salt.id))
        flour_form = self._get_product_form_update(2)
        flour_form["weight"].send_keys("1")
        submit.click()

        # Assert changes
        apple_pie2 = Recipe.objects.get(pk=apple_pie.pk)
        self.assertEqual(apple_pie2.name, apple_pie.name + "2")
        self.assertEqual(apple_pie2.description, apple_pie.description + "2")
        self.assertEqual(Product.objects.get(pk=apple_product.pk).weight, 700)
        self.assertEqual(Product.objects.get(pk=sugar_product.pk).have_recipe.id, salt.id)
        self.assertEqual(Product.objects.get(pk=flour_product.pk).weight, 1150)

    def _get_recipe_form_controls(self):
        name = self.driver.find_element_by_name("name")
        description = self.driver.find_element_by_name("description")
        submit = self.driver.find_element_by_css_selector("[type=submit]")
        return name, description, submit

    def _get_total_forms(self):
        return int(
            self.driver.find_element_by_name("form-TOTAL_FORMS").get_attribute("value")
        )

    def _get_total_forms_update(self):
        return int(
            self.driver.find_element_by_name("belong_recipe-TOTAL_FORMS").get_attribute("value")
        )

    def _add_product_form(self):
        self.driver.find_element_by_css_selector("#add-form").click()

    def _get_product_form(self, i):
        return {
            "have_recipe": self.driver.find_element_by_name(f"form-{i}-have_recipe"),
            "weight": self.driver.find_element_by_name(f"form-{i}-weight"),
        }

    def _get_product_form_update(self, i):
        return {
            "have_recipe": self.driver.find_element_by_name(f"belong_recipe-{i}-have_recipe"),
            "weight": self.driver.find_element_by_name(f"belong_recipe-{i}-weight"),
        }

    def _add_product(self, have_recipe, weight):
        total_forms = self._get_total_forms()
        self._add_product_form()
        self.assertEqual(self._get_total_forms(), total_forms + 1)
        product_form = self._get_product_form(total_forms)
        Select(product_form["have_recipe"]).select_by_value(str(have_recipe))
        product_form["weight"].clear()
        product_form["weight"].send_keys(weight)
