from django.contrib import admin
from django.urls import path, include

from .views import MainView

urlpatterns = [
    path('main_view/', MainView.as_view(), name='main_view'),
]