from django.urls import path
from SentimentApp import views

urlpatterns = [
    path('', views.handleRequest, name='handleRequest'),
    # Add more URL patterns as needed
]