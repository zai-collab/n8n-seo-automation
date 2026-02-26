from django.urls import path

from . import views

app_name = 'kw'

urlpatterns = [
  path('clusters/', views.cluster_list, name='cluster_list'),
  path('clusters/create/', views.cluster_create, name='cluster_create'),
  path('clusters/<int:pk>/edit/', views.cluster_edit, name='cluster_edit'),
  path('clusters/<int:pk>/delete/', views.cluster_delete, name='cluster_delete'),

  path('keywords/', views.keyword_list, name='keyword_list'),
  path('keywords/create/', views.keyword_create, name='keyword_create'),
  path('keywords/<int:pk>/edit/', views.keyword_edit, name='keyword_edit'),
  path('keywords/<int:pk>/delete/', views.keyword_delete, name='keyword_delete'),
  
  path('keywords/research/', views.keyword_research, name='keyword_research'),
  path('keywords/<int:pk>/analyze/', views.keyword_analyze, name='keyword_analyze'),
]