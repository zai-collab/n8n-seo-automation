from django.urls import path

from . import views

app_name = 'backlink'

urlpatterns = [
  path('', views.backlink_list, name='backlink_list'),
]