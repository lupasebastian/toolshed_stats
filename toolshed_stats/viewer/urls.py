from django.contrib import admin
from django.urls import path, include

from .views import MainView, PlayerDetailView

urlpatterns = [
    path('main_view/', MainView.as_view(), name='main_view'),
    path('player/<int:pk>/', PlayerDetailView.as_view(), name='player_detail_view')
]