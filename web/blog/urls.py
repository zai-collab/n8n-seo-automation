from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
  path('metadata/', views.metadata_list, name='metadata_list'),
  path('<int:pk>/create', views.blog_create, name='blog_create'),
]