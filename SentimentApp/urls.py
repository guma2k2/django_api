from django.urls import path
from SentimentApp import views

urlpatterns = [
    path('', views.handleRequest, name='handleRequest'),
    path('/admin', views.handleRequestAdmin, name='handleRequestAdmin'),
    # Add more URL patterns as needed
]