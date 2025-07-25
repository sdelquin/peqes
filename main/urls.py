"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path

import shared.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('404/', shared.views.custom_404),
    path('404/test/', shared.views.test_404),
    path('api/', include('api.urls')),
    path('docs/', include('docs.urls')),
    path('', include('joints.urls')),
]

handler404 = 'shared.views.custom_404'
