from django.urls import path
from SentimentApp import views

urlpatterns = [
    path('', views.handleRequest, name='handleRequest'),
    path('/admin', views.handleRequestAdmin, name='handleRequestAdmin'),
    path('/admin/<int:id>', views.handleRequestWithID, name='handleRequestWithID'),
    # Add more URL patterns as needed
]