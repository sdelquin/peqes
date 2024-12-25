from django.urls import path

from . import views

appname = 'joints'

urlpatterns = [
    path('<str:url_path>/', views.plugin, name='plugin'),
]
