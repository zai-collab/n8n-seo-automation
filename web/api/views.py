import json

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blog.models import Metadata
from kw.models import Cluster, Keyword


@csrf_exempt
@require_POST
def keyword_research_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  seed_keyword = data.get("seed_keyword")
  clusters = data.get("clusters")

  if not seed_keyword or not clusters:
    return HttpResponseBadRequest("Missing Required Fields")

  for cluster in clusters:
    name = cluster.get("cluster")
    intent = cluster.get("intent")
    keywords = cluster.get("keywords")

    cluster = Cluster.objects.create(
      name=name,
      intent=intent,
      seed_keyword=seed_keyword
    )

    bulkOps = []
    for keyword in keywords:
      bulkOps.append(
        Keyword(
          cluster=cluster,
          keyword=keyword.get("keyword"),
          search_volume=keyword.get("search_volume"),
          cpc=keyword.get("cpc"),
          competition=keyword.get("competition")
        )
      )

    Keyword.objects.bulk_create(bulkOps)

  return HttpResponse("success")


@csrf_exempt
@require_POST
def keyword_analyze_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  metadata = data.get("metadata")

  if not metadata:
    return HttpResponseBadRequest("Missing Required Fields")

  id = metadata.get("keyword_id")
  keyword = Keyword.objects.get(pk=id)

  Metadata.objects.create(
    title=metadata.get("title"),
    intent=metadata.get("intent"),
    meta_description=metadata.get("meta_description"),
    outline=metadata.get("outline"),
    must_cover=metadata.get("must_cover"),
    secondary_keywords=metadata.get("secondary_keywords"),
    keyword=keyword,
  )

  keyword.is_analyzed = True
  keyword.save()

  return HttpResponse("success")
