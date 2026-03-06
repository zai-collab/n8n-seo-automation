from django.urls import path

from . import views


app_name = 'api'

urlpatterns = [
    path("keyword-research-webhook/", views.keyword_research_webhook),
    path("keyword-analyze-webhook/", views.keyword_analyze_webhook),
    path("keyword-analyze-cron-job-webhook/", views.keyword_analyze_cron_job_webhook),
    path("image-upload-webhook/", views.image_upload_webhook),
    path("blog-post-webhook/", views.blog_post_webhook),
    path("backlinks-webhook/", views.backlinks_webhook),
    path("content-webhook/", views.content_webhook),
    path("outreach-webhook/", views.outreach_webhook),
]