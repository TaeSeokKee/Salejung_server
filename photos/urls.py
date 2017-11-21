from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^photo/post/', views.addPhoto, name='addPhoto'),
    url(r'^latlng/post/', views.getItemByLngLat, name='getItemByLngLat'),
    url(r'^userId/post/', views.getItemByUserId, name='getItemByUserId'),
    url(r'^', views.index, name='index'),
]
