import json
import random
import time

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from post.models import Metadata, Blog
from kw.models import Keyword


@csrf_exempt
@require_POST
def keyword_research_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  seed_keyword = data.get("seedKeyword")
  keywords = data.get("keywords")

  if not seed_keyword or not keywords:
    return HttpResponseBadRequest("Missing Required Fields")

  bulkOps = []
  for keyword in keywords:
    bulkOps.append(
      Keyword(
        seed_keyword=seed_keyword,
        keyword=keyword.get("keyword"),
        search_volume=keyword.get("searchVolume"),
        cpc=keyword.get("cpc"),
        competition=keyword.get("competition"),
        keyword_difficulty=keyword.get("keywordDifficulty"),
        search_intent=keyword.get("searchIntent"),
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


@csrf_exempt
@require_POST
def blog_post_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  blog = Blog.objects.create(
    title=data.get("title"),
    slug=data.get("slug"),
    content=data.get("content"),
    featured_image_alt=data.get("alt_text"),
  )

  return JsonResponse({"blog_id": blog.id}, status=201)


@csrf_exempt
@require_POST
def image_upload_webhook(request):
  blog_id = request.POST.get("blog_id")
  blog = Blog.objects.get(pk=int(blog_id))

  fp = request.FILES["file"]
  ext = request.POST.get("extension")

  timestamp = int(time.time() * 1000)
  rand = random.randint(1000, 9999)

  path = f"uploads/blog/{timestamp}_{rand}.{ext}"
  path = default_storage.save(path, ContentFile(fp.read()))

  blog.featured_image_path = path
  blog.save()

  return HttpResponse("success")