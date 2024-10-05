from django.urls import path
from rest_framework.authtoken import views as auth
from . import views

urlpatterns = [
    path(r'^$', views.index, name='index'),
]
