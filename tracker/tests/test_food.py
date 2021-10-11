from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.shortcuts import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tracker.models import Food, Recipe, Product


class FoodTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # * Requires geckodriver binary
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """Test-wide common setup."""
        pass
        # Create 3 Food, Product and Recipe objects
        # f1 = Food.objects.create(name="Apple", calories=72)
        # f2 = Food.objects.create(name="Orange", calories=32)
        # f3 = Food.objects.create(name="Banana", calories=84)

    def test_create_food(self):
        self.driver.get(self.live_server_url + reverse("tracker:add_food"))
        name_field = self.driver.find_element_by_name("name")
        calories_field = self.driver.find_element_by_name("calories")
        submit_button = self.driver.find_element_by_name("Submit")

        name_field.send_keys("Apple" + Keys.ENTER)
        calories_field.send_keys("72" + Keys.ENTER)
        submit_button.click()

        self.assertEqual(
            self.driver.current_url, self.live_server_url + reverse("tracker:food")
        )
        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_list_food(self):
        f1 = Food.objects.create(name="Apple", calories=72)
        r1 = Recipe.objects.create(name="Apple")
        p1 = Product.objects.create(weight=100, recipe=r1, have_food=f1)
        
        self.driver.get(self.live_server_url + reverse('tracker:food'))
        table_rows = self.driver.find_elements_by_css_selector('tr')

        self.assertEqual(len(table_rows) - 1, Recipe.objects.count())
