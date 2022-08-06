"""retire_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    # internal management
    path('admin/', admin.site.urls),

    # tarot webapp
    path('tarot/', include(('tarot_app.urls', 'tarot_app'))),
    path('tarot/', include(('accounts.urls', 'tarot_app'))),
    path('tarot/convert/', include('guest_user.urls')),

    # code immersion webapp
    path('code_immersion/', include(('code_immersion_app.urls', 'ci'))),

    # google analytics
    re_path('djga/', include('google_analytics.urls')),
]
