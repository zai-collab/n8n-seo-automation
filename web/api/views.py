import json
import random
import time

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from backlink.models import Backlink, Content, Outreach
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

  data = data.get("data")

  if not data:
    return HttpResponseBadRequest("Missing Required Fields")

  for item in data:
    id = item.get("keyword_id")
    keyword = Keyword.objects.get(pk=id)

    if not keyword:
      return HttpResponseBadRequest("Keyword not found")

    metadata = item.get("metadata")

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
def keyword_analyze_cron_job_webhook(request):
  keywords = Keyword.objects.filter(status='approved')

  return JsonResponse({"data": [keyword.serialize() for keyword in keywords]})


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


@csrf_exempt
@require_POST
def backlinks_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  backlinks = data.get("backlinks")

  if not backlinks:
    return HttpResponseBadRequest("Missing Required Fields")

  keyword_id = data.get("id")
  keyword = Keyword.objects.get(pk=keyword_id)
  if not keyword:
    return HttpResponseBadRequest("Keyword not found")

  for backlink in backlinks:
    Backlink.objects.create(
      keyword=keyword,
      domain_from=backlink.get("domainFrom", ""),
      domain_rank=backlink.get("domainRank") or 0,
      url_from=backlink.get("urlFrom", ""),
      url_to=backlink.get("urlTo", ""),
      url_to_redirect_target=backlink.get("urlToRedirectTarget", ""),
      links_count=backlink.get("linksCount") or 0,
      semantic_location=backlink.get("semanticLocation", ""),
      page_title=backlink.get("pageTitle", ""),
      anchor_text=backlink.get("anchor", ""),
      alt_text=backlink.get("alt", ""),
      backlink_spam_score=backlink.get("backlinkSpamScore") or 0,
      item_type=backlink.get("itemType", ""),
      is_indirect_link=backlink.get("isIndirectLink") or False,
      dofollow=backlink.get("dofollow") or False,
      is_broken=backlink.get("isBroken") or False,
      is_lost=backlink.get("isLost") or False,
      is_new=backlink.get("isNew") or False,
      first_seen=backlink.get("firstSeen"),
      last_seen=backlink.get("lastSeen"),
    )

  return HttpResponse("success")


@csrf_exempt
@require_POST
def content_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  data = data.get("data")
  type = data.get("type")

  if type == 'topic':
    topics = data.get("topics")

    if not topics:
      return HttpResponseBadRequest("Missing Required Fields")

    backlink_id = data.get("id")
    backlink = Backlink.objects.get(pk=backlink_id)
    if not backlink:
      return HttpResponseBadRequest("Backlink not found")

    Content.objects.create(
      backlink=backlink,
      topics=topics,
      anchor_text=data.get("anchorText"),
      target_url=data.get("targetUrl"),
      author=data.get("author"),
    )
  else:
    content_id = data.get("id")
    content = Content.objects.get(pk=content_id)
    if not content:
      return HttpResponseBadRequest("Content not found")

    content.title = data.get("title")
    content.content_html = data.get("contentHtml")
    content.save()
  
  return HttpResponse("success")
  

@csrf_exempt
@require_POST
def outreach_webhook(request):
  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return HttpResponseBadRequest("Invalid Request Body")

  content_id = data.get("id")
  content = Content.objects.get(pk=content_id)
  if not content:
    return HttpResponseBadRequest("Missing Required Fields")

  Outreach.objects.create(
    content=content,
    subject=data.get("subject"),
    body=data.get("body"),
  )

  return HttpResponse("success")
