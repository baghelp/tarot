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
    #path('one_time_investment/<str:id>', views.onetimeinvestment, name='onetimeinvestment'),
    #path('one_time_investment', views.onetimeinvestment, name='onetimeinvestment'),
    #path('recurring_investment/<str:id>', views.recurringinvestment, name='recurringinvestment'),
    #path('recurring_investment', views.recurringinvestment, name='recurringinvestment'),
    path('goal/<str:id>', views.goal, name='goal'),
    path('goal', views.goal, name='goal'),

]
