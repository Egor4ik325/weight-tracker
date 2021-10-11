from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Home url
    path('', views.HomeView.as_view(), name='home'),

    # Food
    path('food/', views.food, name='food'),
    path('add_food/', views.add_food, name='add_food'),
    # Edit food or recipe
    path('edit_food/<int:food_id>/', views.edit_food, name='edit_food'),

    # Recipe
    path('add_recipe/', views.add_recipe, name='add_recipe'),

    # Track (records)
    path('track/', views.track, name='track'),
    path('track/<date>/', views.track, name='track_date'),
    path('add_record/<int:section>/', views.add_record, name='add_record'),
]
