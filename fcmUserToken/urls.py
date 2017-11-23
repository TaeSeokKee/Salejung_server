from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^getFcmUserToken/', views.getFcmUserToken, name='getFcmUserToken'),
    url(r'^setFcmUserToken/', views.setFcmUserToken, name='setFcmUserToken'),
]
