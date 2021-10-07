from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    # Home url
    path('', views.HomeView.as_view(), name='home'),

    # Food urls
    path('food/', views.food, name='food'),
    path('add_food/', views.add_food, name='add_food'),
    path('edit_food/<int:food_id>/', views.edit_food, name='edit_food'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:food_id>/', views.edit_recipe, name="edit_recipe"),

    # Track urls
    path('track/', views.track, name='track'),
    path('track/<date>/', views.track, name='track_date'),
    path('add_record/<int:section>/', views.add_record, name='add_record'),

    # Test urls
    path('testtrans/', views.TestTransView.as_view(), name='testtrans'),


    # testing class-based views
    # path('view_recipe/<int:recipe_pk>/', views.view_recipe, name='view_recipe'),
    # path('add_product/<int:recipe_pk>/', views.add_product, name='add_product'),
    # path('view_recipe/<int:recipe_pk>/', views.ProductListView.as_view(), name='view_recipe'),
    # path('add_product/<int:recipe_pk>/', views.ProductAddView.as_view(), name='add_product'),
]
