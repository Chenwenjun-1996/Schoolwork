from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('display/', views.display, name="display"),
    path('draw_map/', views.drawMap, name="draw_map"),
]