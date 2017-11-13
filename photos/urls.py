from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^photo/post/', views.postPhoto, name='photo-post'),
    url(r'^latlng/post/', views.postLatLng, name='latlng-post'),
    url(r'^', views.index, name='index'),
]
