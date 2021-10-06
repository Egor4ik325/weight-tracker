from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.forms import formset_factory, modelformset_factory
import datetime

from pprint import pprint

from .models import Food, Product, Recipe, Record
from .forms import FoodForm, RecipeForm, ProductForm, RecordForm
from .forms import ProductFormSet


# def view_recipe(request, recipe_pk):
#     r = Recipe.objects.get(pk=recipe_pk)
#     prods = r.belong_recipe.all()
#     context = {'products': prods, 'recipe_pk': recipe_pk}
#     return render(request, 'tracker/view_recipe.html', context)


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

# Create your views here.

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
            # Create food
            f = form.save()
            # Create recipe
            r = Recipe.objects.create(name=f.name)
            # Create product
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
        # product_formset = ProductFormSet(data=request.POST)
        #and product_formset.is_valid()
        if recipe_form.is_valid():
            created_recipe = recipe_form.save()
            return redirect(reverse('tracker:add_recipe_food', args=[created_recipe.id]))
        else:
            context = {'recipe_form': recipe_form}
            return render(request, 'tracker/add_recipe.html', context)
    else:
        raise Exception("Undefined HTTP request method.")

def add_recipe_food(request, recipe_id):
    if request.method == 'GET':
        # Create ProductForm with parent recipe
        # r = Recipe.objects.get(pk=recipe_id)
        # initial={'recipe': recipe_id}
        product_form = ProductForm()
        product_form.fields['have_recipe'].choices = [(r, str(r))
                                                      for r in Recipe.objects.exclude(pk=recipe_id)]
        # product_form = ProductForm()

        # product_form.fields['have_recipe'].choices = [
        #     (p, str(p)) for p in Recipe.objects.exclude(pk=recipe_id)
        # ]

        context = {'product_form': product_form, 'recipe_id': recipe_id}
        return render(request, 'tracker/add_recipe_food.html', context)
    elif request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        product_form.fields['have_recipe'].choices = [(r, str(r))
                                                      for r in Recipe.objects.exclude(pk=recipe_id)]
        if product_form.is_valid():
            # product_form.save()
            created_product = product_form.save(commit=False)
            r = Recipe.objects.get(pk=recipe_id)
            # set product parent
            created_product.recipe = r
            created_product.save()
            return redirect(reverse('tracker:add_recipe_food', args=[recipe_id]))
        else:
            context = {'product_form': product_form, 'recipe_id': recipe_id}
            return render(request, 'tracker/add_recipe_food.html', context)
    else:
        raise Exception("Undefined HTTP request method.")

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
    r = Recipe.objects.get(pk=food_id)
    prods = r.belong_recipe.all()
    # ProductFormSet = modelformset_factory(Product, fields=['have_recipe', 'weight'], extra=0)

    if request.method == 'GET':
        recipe_form = RecipeForm(instance=r)

        product_formset = ProductFormSet(queryset=prods)
        # ProductFormSet = formset_factory(ProductForm)
        # product_formset = ProductFormSet()

        # product_forms = [ProductForm(instance=p) for p in prods]
        # context = {'recipe_form': recipe_form, 'product_forms': product_forms, 'recipe_id': food_id}
        context = {'recipe_form': recipe_form, 'product_formset': product_formset, 'recipe_id': food_id}
        return render(request, 'tracker/edit_recipe.html', context)
    elif request.method == 'POST':
        pprint(request.POST)
        recipe_form = RecipeForm(data=request.POST, instance=r)
        product_formset = ProductFormSet(request.POST, queryset=prods)
        # product_forms = [ProductForm(data=request.POST, instance=p) for p in prods]
        # if recipe_form.is_valid() and all([pf.is_valid() for pf in product_forms]):
        if recipe_form.is_valid() and product_formset.is_valid():
            # Save changes to all objects/forms
            recipe_form.save()
            product_formset.save()
            # for i in range(len(product_forms)):
            #     product_forms[i].save()
            return redirect('tracker:food')
        else:
            context = {'recipe_form': recipe_form, 'product_formset': product_formset, 'recipe_id': food_id}
            return render(request, 'tracker/edit_recipe.html', context)
    else:
        raise Exception("Undefined HTTP request method.")

# def edit_food(request, food_id):
#     recipe = Recipe.objects.get(pk=food_id)
#     if len(recipe.belong_recipe.all()) == 1:
#         # The recipe is a food (discrete/primitive)
#         food = recipe.belong_recipe.all()[0].food
#         if request.method == 'GET':
#             form = FoodForm(food)
#             context = {'form': form, 'food_id': food_id}
#             return render(request, 'tracker/edit_food.html', context)
#         elif request.method == 'POST':
#             form = FoodForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('tracker:food')
#             else:
#                 context = {'form': form}
#                 return render(request, 'tracker/edit_food.html', context)
#         else:
#             raise Exception("Undefined HTTP request method.")
#     else:
#         # The recipe is a food (complex)
#         pass

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

# def track(request):
#     # current time
#     return track(request, datetime.datetime.now() + datetime.timedelta(hours=3))

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
