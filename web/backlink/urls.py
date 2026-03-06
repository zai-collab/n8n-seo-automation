from django.urls import path

from . import views

app_name = 'backlink'

urlpatterns = [
  path('', views.backlink_list, name='backlink_list'),
  path('content/', views.content_list, name='content_list'),
  path('content/<int:pk>/topic/', views.content_topic, name='content_topic'),
  path('content/<int:pk>/guest-post/', views.content_guest_post, name='content_guest_post'),
  path('content/<int:pk>/outreach/', views.content_outreach, name='content_outreach'),
  path('content/<int:pk>/delete/', views.content_delete, name='content_delete'),
]