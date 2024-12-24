from django.urls import path

from . import views

appname = 'urls'

urlpatterns = [
    path('<str:url_path>/', views.plug, name='plug'),
]
