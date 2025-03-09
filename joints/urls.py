from django.urls import path

from . import views

app_name = 'joints'

urlpatterns = [
    path('', views.shorten, name='shorten'),
    path('<str:url_path>/', views.plugin, name='plugin'),
]
