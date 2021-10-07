from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.forms import formset_factory, modelformset_factory
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
import datetime

from pprint import pprint

from .models import Food, Product, Recipe, Record
from .forms import FoodForm, RecipeForm, ProductForm, RecordForm
from .forms import ProductFormSet, InlineProductFormSet


def add_product(request, recipe_pk):
    if request.method == 'GET':
        formset = ProductFormSet(queryset=Product.objects.none())
        context = {'product_formset': formset, 'recipe_pk': recipe_pk}
        return render(request, 'tracker/add_product.html', context)
    elif request.method == 'POST':
        formset = ProductFormSet(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('tracker:food'))
        else:
            return render(request, 'tracker/add_product.html', {'product_formset': formset, 'recipe_pk':recipe_pk})
    else:
        pass

class TestTransView(TemplateView):
    template_name = "tracker/testtrans.html"

class HomeView(TemplateView):
    template_name = "tracker/index.html"

def food(request):
    """ Responds with the table of custom food (recipes). """
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'tracker/food.html', context)

def testtrans(request):
    return render(request, 'tracker/testtrans.html')

def add_food(request):
    """ Responds with the form to add new food. """
    if request.method == 'GET':
        form = FoodForm()
        context = {'form': form}
        return render(request, 'tracker/add_food.html', context)
    elif request.method == 'POST':
        form = FoodForm(data=request.POST)
        if form.is_valid():
            # Because user will be choosing eaten food from recipes objects
            # we need to create a basic product and recipe objects together
            # with food object so that it can choose them.
            f = form.save()
            r = Recipe.objects.create(name=f.name)
            p = Product.objects.create(have_food=f, recipe=r)
            return redirect('tracker:food')
        else:
            context = {'form': form}
            return render(request, 'tracker/add_food.html', context)
    else:
        raise Exception("Undefined HTTP request method.")

def add_recipe(request):
    """ The add recipe page consist of a recipe name/desc form and a set of product forms. """
    if request.method == 'GET':
        recipe_form = RecipeForm()
        product_formset = ProductFormSet(queryset=Product.objects.none())
        context = {'recipe_form': recipe_form, 'product_formset': product_formset}
        return render(request, 'tracker/add_recipe.html', context)
    elif request.method == 'POST':
        recipe_form = RecipeForm(data=request.POST)
        product_formset = ProductFormSet(data=request.POST)

        # Is recipe form is valid (recipe name and description)
        if recipe_form.is_valid():
            # Is recipe attached products are selected valid
            if product_formset.is_valid():
                recipe_created = recipe_form.save()

                for form in product_formset.forms:
                    # Bind all created products to the form
                    product = form.save(commit=False)
                    product.recipe = recipe_created
                    product.save()

                return redirect(reverse('tracker:food'))
            else:
                return HttpResponseBadRequest("Invalid product forms!")
        else:
            return HttpResponseBadRequest("Invalid recipe form!")

def edit_food(request, food_id):
    r = Recipe.objects.get(pk=food_id)
    if len(r.belong_recipe.all()) == 1:
        p = r.belong_recipe.all()[0]
        f = p.have_food
        # The recipe is a discrete
        if request.method == 'GET':
            form = FoodForm(instance=f)
            context = {'form': form, 'food_id': food_id}
            return render(request, 'tracker/edit_food.html', context)
        elif request.method == 'POST':
            form = FoodForm(data=request.POST, instance=f)
            if form.is_valid():
                form.save()
                return redirect('tracker:food')
            else:
                context = {'form': form, 'food_id': food_id}
                return render(request, 'tracker/edit_food.html', context)
        else:
            raise Exception("Undefined HTTP request method.")
    else:
        # The recipe is complex
        return edit_recipe(request, food_id)

def edit_recipe(request, food_id):
    """Patch given recipe with the given request POST data."""
    # Handle changes
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, pk=food_id)
        recipe_form = RecipeForm(data=request.POST, instance=recipe)
        product_formset = InlineProductFormSet(data=request.POST, instance=recipe)
        if recipe_form.is_valid():
            if product_formset.is_valid():
                recipe_form.save()
                product_formset.save()
                return redirect(reverse('tracker:food'))
            else:
                return HttpResponseBadRequest("Invalid product formset data.")
        else:
            return HttpResponseBadRequest("Invalid recipe form data.")

    # Render form
    recipe = get_object_or_404(Recipe, pk=food_id)
    recipe_form = RecipeForm(instance=recipe)
    product_formset = ProductFormSet(queryset=recipe.belong_recipe.all())
    context = {
        'recipe_form': recipe_form,
        'product_formset': product_formset,
        'food_id': food_id,
    }
    return render(request, 'tracker/edit_recipe.html', context)

def track(request, date = None):
    # Redirect to the same URL with current date
    if date is None:
        cur_date = datetime.datetime.now() + datetime.timedelta(hours=3)
        return redirect('/track/' + str(cur_date.date()))

    # Convert date string to date object
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    # 1. Make all computations (prepare for template usage)
    # 2. Use/iterate all prepared data
    section_names = ['breakfast', 'second breakfast', 'dinner', 'lunch', 'supper']
    sections_records = [Record.objects.filter(date_added=date, section=i) for i in range(1, 6)]
    section_totals = [sum([record.total for record in records])
                      for records in sections_records]
    total = sum(section_totals)

    context = {'sections': zip(section_names, section_totals, sections_records, range(1, 6)),
               'total': total,
               'track_date': date}
    return render(request, 'tracker/track.html', context)

def add_record(request, section):
    if request.method == 'GET':
        form = RecordForm()
        context = {'form': form, 'section': section}
        return render(request, 'tracker/add_record.html', context)
    elif request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            added_record = form.save(commit=False)
            added_record.section = section
            added_record.save()
            return redirect('tracker:track')
        else:
            context = {'form': form}
            return render(request, 'tracker/add_record.html', context)
    else:
        raise Exception("Undefined HTTP request method.")

# def view_recipe(request, recipe_pk):
#     r = Recipe.objects.get(pk=recipe_pk)
#     prods = r.belong_recipe.all()
#     context = {'products': prods, 'recipe_pk': recipe_pk}
#     return render(request, 'tracker/view_recipe.html', context)
