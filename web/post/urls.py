from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
  path('metadata/', views.metadata_list, name='metadata_list'),
  path('metadata/approve/', views.metadata_approve, name='metadata_approve'),
  path('metadata/<int:pk>/edit/', views.metadata_edit, name='metadata_edit'),

  path('blogs/', views.blog_list, name='blog_list'),
  path('blogs/<int:pk>/create/', views.blog_create, name='blog_create'),
  path('blogs/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
  path('blogs/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]