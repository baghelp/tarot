from django.urls import path, include
from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', view=views.home, name='home'),
    path('about', view=views.about, name='about'),
    path('login', view=views.login, name='login'),
    path('convert', view=views.convert, name='convert'),

]
