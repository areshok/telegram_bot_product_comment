
from django.contrib import admin
from django.urls import path, include
from .views import index, comments, comment_detail

app_name = 'product'

urlpatterns = [
    path('', index, name='index'),
    path('comments', comments, name='comments'),
    path('comments/<id>', comment_detail , name='comment_detail'),
]
