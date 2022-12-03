from django.urls import path, include
from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', view=views.home, name='home'),
    path('about', view=views.about, name='about'),
    path('income_and_expenses/<str:id>', views.workcashflow, name='workcashflow'),
    path('income_and_expenses', views.workcashflow, name='workcashflow'),
    path('change_in_income/<str:id>', views.changeinincome, name='changeinincome'),
    path('change_in_income', views.changeinincome, name='changeinincome'),
    path('change_in_expenses/<str:id>', views.changeinexpenses, name='changeinexpenses'),
    path('change_in_expenses', views.changeinexpenses, name='changeinexpenses'),
    path('record_observation/<str:id>', views.recordobservation, name='recordobservation'),
    path('record_observation', views.recordobservation, name='recordobservation'),
    path('goal/<str:id>', views.goal, name='goal'),
    path('goal', views.goal, name='goal'),

]
