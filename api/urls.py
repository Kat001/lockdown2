from django.contrib import admin
from django.urls import path,include

from .views import CreateBookAPI
from . import views

urlpatterns = [
  
    path('add-book/',views.CreateBookAPI.as_view()),   
]