from django.urls import path

from . import views

app_name = 'kw'

urlpatterns = [
  path('keywords/', views.keyword_list, name='keyword_list'),
  path('keywords/<int:pk>/edit/', views.keyword_edit, name='keyword_edit'),
  path('keywords/<int:pk>/backlinks/', views.keyword_backlinks, name='keyword_backlinks'),
  path('keywords/<int:pk>/delete/', views.keyword_delete, name='keyword_delete'),
  path('keywords/approve/', views.keyword_approve, name='keyword_approve'),
  
  path('keywords/research/', views.keyword_research, name='keyword_research'),
  path('keywords/<int:pk>/analyze/', views.keyword_analyze, name='keyword_analyze'),
]