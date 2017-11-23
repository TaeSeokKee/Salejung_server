from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^addItem/', views.addItem, name='addItem'),
    url(r'^getItemInfoByLngLat/', views.getItemInfoByLngLat, name='getItemInfoByLngLat'),
    url(r'^getItemLocationByLngLat/', views.getItemLocationByLngLat, name='getItemLocationByLngLat'),
    url(r'^getItemInfoByUserId/', views.getItemInfoByUserId, name='getItemInfoByUserId'),
    url(r'^', views.index, name='index'),
]
