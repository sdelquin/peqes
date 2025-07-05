from django.urls import path

from . import views

app_name = 'docs'

urlpatterns = [
    path('api/', views.api_docs, name='api'),
    path('disclaimer/', views.disclaimer_docs, name='disclaimer'),
]
