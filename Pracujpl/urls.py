from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.pracuj),
    path(r'^sendmail/$', views.sendmail, name='sendmail'),
]
