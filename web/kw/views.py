import os

from urllib.parse import urljoin

import requests

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Keyword


@staff_member_required
def keyword_list(request):
  query = request.GET.get('query', '').strip()

  keywords = Keyword.objects.order_by('-created_at')

  if query:
    keywords = keywords.filter(keyword__icontains=query)

  paginator = Paginator(keywords, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    "page": page,
    "query": query,
  }

  return render(request, 'index.html', context)


@staff_member_required
def keyword_edit(request, pk: int):
  keyword_item = get_object_or_404(Keyword, pk=pk)

  if request.method == 'POST':
    keyword = request.POST.get('keyword', '').strip()
    search_volume = request.POST.get('search_volume') or 0
    cpc = request.POST.get('cpc') or 0
    competition = request.POST.get('competition', '') or 0
    keyword_difficulty = request.POST.get('keyword_difficulty', '') or 0

    if keyword:
      keyword_item.keyword = keyword
      keyword_item.search_volume = int(search_volume or 0)
      keyword_item.cpc = cpc or 0
      keyword_item.competition = competition or 0
      keyword_item.keyword_difficulty = keyword_difficulty or 0
      keyword_item.is_approved = False
      keyword_item.is_analyzed = False
      keyword_item.save()
      return redirect('kw:keyword_list')

  context = {
    'keyword': keyword_item,
  }

  return render(request, 'edit.html', context)


@staff_member_required
def keyword_delete(request, pk: int):
  keyword = get_object_or_404(Keyword, pk=pk)
  keyword.delete()
  return redirect('kw:keyword_list')


@staff_member_required
@require_POST
def keyword_approve(request):
  keyword_ids = request.POST.get('selected_keywords', '').split(',')
  keywords = Keyword.objects.filter(pk__in=keyword_ids)
  keywords.update(is_approved=True)
  return redirect('kw:keyword_list')


@staff_member_required
@require_POST
def keyword_research(request):
  seed_keyword = request.POST.get('keyword', '').strip()
  if not seed_keyword:
    return redirect('/')

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_KEYWORD_RESEARCH_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"keyword": seed_keyword},
    timeout=15
  )

  return redirect("/")

@staff_member_required
@require_POST
def keyword_analyze(request, pk: int):
  keyword = get_object_or_404(Keyword, pk=pk)
  if not keyword:
    return redirect('/')

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_KEYWORD_ANALYZE_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"data": keyword.serialize()},
    timeout=15
  )

  return redirect("kw:keyword_list")


@staff_member_required
@require_POST
def keyword_backlinks(request, pk: int):
  keyword = get_object_or_404(Keyword, pk=pk)
  if not keyword:
    return redirect('/')

  requests.post(
    urljoin(os.getenv('N8N_BASE_URL'), os.getenv('N8N_KEYWORD_BACKLINKS_WEBHOOK_URL')),
    headers={"Webhook-Token": settings.WEBHOOK_TOKEN},
    json={"data": keyword.serialize()},
    timeout=15
  )

  return redirect("kw:keyword_list")
  