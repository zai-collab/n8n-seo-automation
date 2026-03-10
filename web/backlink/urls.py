from django.urls import path

from . import views

app_name = 'backlink'

urlpatterns = [
  path('', views.backlink_list, name='backlink_list'),
  path('approve/', views.backlink_approve, name='backlink_approve'),
  path('content/', views.content_list, name='content_list'),
  path('content/approve/', views.content_approve, name='content_approve'),
  path('content/<int:pk>/topic/', views.content_topic, name='content_topic'),
  path('content/<int:pk>/guest-post/', views.content_guest_post, name='content_guest_post'),
  path('content/<int:pk>/outreach/', views.content_outreach, name='content_outreach'),
  path('content/<int:pk>/edit/', views.content_edit, name='content_edit'),
  path('content/<int:pk>/delete/', views.content_delete, name='content_delete'),
  
  path('outreach/', views.outreach_list, name='outreach_list'),
  path('outreach/approve/', views.outreach_approve, name='outreach_approve'),
  path('outreach/<int:pk>/edit/', views.outreach_edit, name='outreach_edit'),
  path('outreach/<int:pk>/delete/', views.outreach_delete, name='outreach_delete'),
]