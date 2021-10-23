from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from tracker.models import Recipe


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
        name = self.driver.find_element_by_name("name")
        description = self.driver.find_element_by_name("description")
        submit = self.driver.find_element_by_css_selector("[type=submit]")
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

    def _get_total_forms(self):
        return int(
            self.driver.find_element_by_name("form-TOTAL_FORMS").get_attribute("value")
        )

    def _add_product_form(self):
        self.driver.find_element_by_css_selector("#add-form").click()

    def _get_product_form(self, i):
        return {
            "have_recipe": self.driver.find_element_by_name(f"form-{i}-have_recipe"),
            "weight": self.driver.find_element_by_name(f"form-{i}-weight"),
        }

    def _add_product(self, have_recipe, weight):
        total_forms = self._get_total_forms()
        self._add_product_form()
        self.assertEqual(self._get_total_forms(), total_forms + 1)
        product_form = self._get_product_form(total_forms)
        Select(product_form["have_recipe"]).select_by_value(str(have_recipe))
        product_form["weight"].clear()
        product_form["weight"].send_keys(weight)
