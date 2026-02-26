import os

from urllib.parse import urljoin

import requests

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Metadata, Blog


@staff_member_required
def metadata_list(request):
  query = request.GET.get('query', '').strip()

  qs = (
    Metadata.objects.all().order_by('-created_at')
  )

  if query:
    qs = qs.filter(Q(title__icontains=query) | Q(meta_description__icontains=query) | Q(intent__icontains=query))

  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    "page": page,
    "query": query,
  }

  return render(request, 'metadata/index.html', context)


@staff_member_required
@require_POST
def blog_create(request, pk: int):
  metadata = Metadata.objects.select_related('keyword').get(pk=pk)

  if not metadata:
    return redirect('post:metadata_list')

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_BLOG_POST_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"metadata": {
      "title": metadata.title,
      "intent": metadata.intent,
      "meta_description": metadata.meta_description,
      "keyword": metadata.keyword.keyword,
      "outline": metadata.outline,
      "must_cover": metadata.must_cover,
      "secondary_keywords": metadata.secondary_keywords,
    }},
    timeout=15
  )

  return redirect("post:metadata_list")


@staff_member_required
def blog_list(request):
  query = request.GET.get('query', '').strip()

  qs = (
    Blog.objects.all().order_by('-created_at')
  )

  if query:
    qs = qs.filter(Q(title__icontains=query))

  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    "page": page,
    "query": query,
  }

  return render(request, 'blog/index.html', context)


@staff_member_required
@require_POST
def blog_delete(request, pk: int):
  blog = get_object_or_404(Blog, pk=pk)

  if blog.featured_image_path:
    if default_storage.exists(blog.featured_image_path):
      default_storage.delete(blog.featured_image_path)

  blog.delete()
  return redirect('post:blog_list')
