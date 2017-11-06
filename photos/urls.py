from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^photos/api/', views.getPostPhoto, name='rest-api'),
    url(r'^', views.index, name='index'),
]
