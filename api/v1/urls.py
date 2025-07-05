from django.urls import path

from . import views

app_name = 'api-v1'

urlpatterns = [
    path('shorten/', views.shorten_url, name='shorten_url'),
]
