from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^addItem/', views.addItem, name='addItem'),
    url(r'^getItemsInfoByLngLat/', views.getItemsInfoByLngLat, name='getItemsInfoByLngLat'),
    url(r'^getItemsLocationByLngLat/', views.getItemsLocationByLngLat, name='getItemsLocationByLngLat'),
    url(r'^getItemById/', views.getItemById, name='getItemById'),
    url(r'^removeItem/', views.removeItem, name='removeItem'),
    url(r'^', views.index, name='index'),
]
