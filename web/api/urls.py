from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path("keyword-research-webhook/", views.keyword_research_webhook),
    path("keyword-analyze-webhook/", views.keyword_analyze_webhook),
    path("image-upload-webhook/", views.image_upload_webhook),
    path("blog-post-webhook/", views.blog_post_webhook),
]