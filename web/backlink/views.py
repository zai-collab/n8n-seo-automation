import os

from urllib.parse import urljoin

import requests

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Backlink, Content, Outreach


@staff_member_required
def backlink_list(request):
  query = request.GET.get('query', '').strip()

  qs = (
    Backlink.objects.order_by('-created_at')
  )
  
  if query:
    qs = qs.filter(
      Q(domain_from__icontains=query) | Q(url_to__icontains=query) | Q(anchor_text__icontains=query) | Q(alt_text__icontains=query)
    )
  
  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    'page': page, 
    'query': query
  }
  
  return render(request, 'backlink/index.html', context)


@staff_member_required
@require_POST
def backlink_approve(request):
  ids = request.POST.get('selected_backlinks', '').split(',')
  backlinks = Backlink.objects.filter(pk__in=ids)
  backlinks.update(status='approved')
  return redirect('backlink:backlink_list')


@staff_member_required
def content_topic(request, pk: int):
  backlink = get_object_or_404(Backlink, pk=pk)
  if not backlink:
    return redirect('backlink:backlink_list')

  data = {
    'type': 'topic',
    'target_url': 'https://www.example.com',
    'author': 'John Doe',
    'anchor_text': 'Example Anchor Text',
    'backlink': backlink.serialize(),
  }

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_CONTENT_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"data": data},
    timeout=15
  )

  return redirect('backlink:backlink_list')


@staff_member_required
def content_list(request):
  query = request.GET.get('query', '').strip()
  status = request.GET.get('status', '').strip()

  qs = Content.objects.select_related('backlink').order_by('-created_at')

  if query:
    qs = qs.filter(
      Q(title__icontains=query)
      | Q(anchor_text__icontains=query)
      | Q(author__icontains=query)
      | Q(target_url__icontains=query)
    )

  if status:
    qs = qs.filter(status=status)

  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    'page': page,
    'query': query,
    'status': status,
  }

  return render(request, 'content/index.html', context)


@staff_member_required
@require_POST
def content_approve(request):
  ids = request.POST.get('selected_content', '').split(',')
  contents = Content.objects.filter(pk__in=ids)
  contents.update(status='approved')
  return redirect('backlink:content_list')


@staff_member_required
def content_guest_post(request, pk: int):
  content = get_object_or_404(Content, pk=pk)
  
  data = {
    'type': 'guest-post',
    'content': content.serialize(),
  }

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_CONTENT_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"data": data},
    timeout=15
  )

  return redirect('backlink:content_list')


@staff_member_required
def content_outreach(request, pk: int):
  content = get_object_or_404(Content, pk=pk)
  
  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_OUTREACH_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"content": content.serialize()},
    timeout=15
  )

  return redirect('backlink:content_list')


@staff_member_required
def outreach_list(request):
  query = request.GET.get('query', '').strip()
  status = request.GET.get('status', '').strip()

  qs = Outreach.objects.select_related('content', 'content__backlink').order_by('-created_at')

  if query:
    qs = qs.filter(
      Q(subject__icontains=query)
      | Q(body__icontains=query)
      | Q(content__title__icontains=query)
      | Q(content__backlink__domain_from__icontains=query)
    )

  if status:
    qs = qs.filter(status=status)

  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    'page': page,
    'query': query,
    'status': status,
  }
  return render(request, 'outreach/index.html', context)


@staff_member_required
@require_POST
def outreach_approve(request):
  ids = request.POST.get('selected_outreach', '').split(',')
  outreachs = Outreach.objects.filter(pk__in=ids)
  outreachs.update(status='approved')
  return redirect('backlink:outreach_list')


@staff_member_required
def outreach_delete(request, pk: int):
  outreach = get_object_or_404(Outreach, pk=pk)
  outreach.delete()
  return redirect('backlink:outreach_list')


@staff_member_required
def content_delete(request, pk: int):
  content = get_object_or_404(Content, pk=pk)
  content.delete()
  return redirect('backlink:content_list')
