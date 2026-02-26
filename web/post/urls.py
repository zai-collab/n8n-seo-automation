from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
  path('metadata/', views.metadata_list, name='metadata_list'),

  path('blogs/', views.blog_list, name='blog_list'),
  path('blogs/<int:pk>/create/', views.blog_create, name='blog_create'),
  path('blogs/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]