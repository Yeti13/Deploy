from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^reg$', views.register),
    url(r'^home$', views.home),
    url(r'^popular$', views.popular),
    url(r'^submit$', views.submit),
    url(r'^like/(?P<page>\w+)*/(?P<id>\d+)$', views.like),
    url(r'^delete/(?P<page>\w+)*/(?P<id>\d+)$', views.delete),
]
