# Self Creating urls for raj

from django.urls import path
from . import views 

urlpatterns = [
 
    path('', views.index, name="index")
]