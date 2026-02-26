import os

from urllib.parse import urljoin

import requests

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Cluster, Keyword


@staff_member_required
def cluster_list(request):
  query = request.GET.get('query', '').strip()

  qs = (
    Cluster.objects.all()
      .annotate(keyword_count=Count('keywords'))
      .order_by('-created_at')
  )

  if query:
    qs = qs.filter(Q(name__icontains=query) | Q(seed_keyword__icontains=query) | Q(intent__icontains=query))

  paginator = Paginator(qs, 10)
  page = paginator.get_page(request.GET.get('page'))

  context = {
    "page": page,
    "query": query,
  }

  return render(request, 'cluster/index.html', context)


@staff_member_required
def cluster_create(request):
  if request.method == 'POST':
    name = request.POST.get('name', '').strip()
    seed_keyword = request.POST.get('seed_keyword', '').strip()
    intent = request.POST.get('intent', '').strip()

    if name and seed_keyword:
      Cluster.objects.create(
        name=name,
        seed_keyword=seed_keyword,
        intent=intent
      )
      return redirect('kw:cluster_list')

  return render(request, 'cluster/edit.html', {'cluster': None})


@staff_member_required
def cluster_edit(request, pk: int):
  cluster = get_object_or_404(Cluster, pk=pk)

  if request.method == 'POST':
    cluster.name = request.POST.get('name', '').strip()
    cluster.seed_keyword = request.POST.get('seed_keyword', '').strip()
    cluster.intent = request.POST.get('intent', '').strip()
    cluster.save()
    return redirect("kw:cluster_list")

  return render(request, 'cluster/edit.html', {'cluster': cluster})


@staff_member_required
def cluster_delete(request, pk: int):
  cluster = get_object_or_404(Cluster, pk=pk)
  cluster.delete()
  return redirect('kw:cluster_list')


@staff_member_required
def keyword_list(request):
  query = request.GET.get('query', '').strip()
  cluster_id = request.GET.get('cluster')

  keywords = Keyword.objects.select_related('cluster').order_by('-created_at')

  selected_cluster = None

  if cluster_id:
    selected_cluster = get_object_or_404(Cluster, pk=cluster_id)
    keywords = keywords.filter(cluster=selected_cluster)

  if query:
    keywords = keywords.filter(keyword__icontains=query)

  paginator = Paginator(keywords, 10)
  page = paginator.get_page(request.GET.get('page'))

  clusters = Cluster.objects.all().order_by('name')

  context = {
    "page": page,
    "query": query,
    "clusters": clusters,
    "selected_cluster": selected_cluster,
    "cluster_id": cluster_id
  }

  return render(request, 'keyword/index.html', context)


@staff_member_required
def keyword_create(request):
  clusters = Cluster.objects.all().order_by('name')

  if request.method == 'POST':
    cluster_id = request.POST.get('cluster_id')
    keyword = request.POST.get('keyword', '').strip()
    search_volume = request.POST.get('search_volume') or 0
    cpc = request.POST.get('cpc') or 0
    competition = request.POST.get('competition', '').strip()

    if cluster_id and keyword:
      cluster = get_object_or_404(Cluster, pk=cluster_id)
      
      Keyword.objects.create(
        cluster=cluster,
        keyword=keyword,
        search_volume=int(search_volume or 0),
        cpc=cpc or 0,
        competition=competition,
      )
      return redirect('kw:keyword_list')

  context = {
    'keyword': None,
    'clusters': clusters
  }

  return render(request, 'keyword/edit.html', context)


@staff_member_required
def keyword_edit(request, pk: int):
  keyword_item = get_object_or_404(Keyword, pk=pk)
  clusters = Cluster.objects.all().order_by('name')

  if request.method == 'POST':
    cluster_id = request.POST.get('cluster_id')
    keyword = request.POST.get('keyword', '').strip()
    search_volume = request.POST.get('search_volume') or 0
    cpc = request.POST.get('cpc') or 0
    competition = request.POST.get('competition', '').strip()

    if cluster_id and keyword:
      keyword_item.cluster = get_object_or_404(Cluster, pk=cluster_id)
      keyword_item.keyword = keyword
      keyword_item.search_volume = int(search_volume or 0)
      keyword_item.cpc = cpc or 0
      keyword_item.competition = competition
      keyword_item.save()
      return redirect('kw:keyword_list')

  context = {
    'keyword': keyword_item,
    'clusters': clusters,
  }

  return render(request, 'keyword/edit.html', context)


@staff_member_required
def keyword_delete(request, pk: int):
  keyword = get_object_or_404(Keyword, pk=pk)
  keyword.delete()
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
    json={"keyword": keyword.serialize()},
    timeout=15
  )

  return redirect("kw:keyword_list")
