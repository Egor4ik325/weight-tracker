from django.contrib import admin
from .models import Food, Product, Recipe, Record

# Register your models here.
admin.site.register(Food)
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(Record)
