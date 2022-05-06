from django.urls import path, include
from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    path('register', views.register_request, name='register'),
    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='tarot_accounts/login.html'), 
        name='login'
    ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(template_name='tarot_accounts/logged_out.html'), 
        name='logout'
    ),
    path(
        'password_change/', 
        auth_views.PasswordChangeView.as_view(template_name='tarot_accounts/password_change_form.html'), 
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='tarot_accounts/password_change_done.html'),
        name='password_change_done',
    ),
]
