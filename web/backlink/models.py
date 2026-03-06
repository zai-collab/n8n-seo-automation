from django.contrib.postgres.fields import ArrayField
from django.db import models

from kw.models import Keyword


class Backlink(models.Model):
  keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='backlinks')
  
  domain_from = models.URLField(blank=True, null=True)
  domain_rank = models.IntegerField()
  url_from = models.URLField(blank=True, null=True)
  url_to = models.URLField(blank=True, null=True)
  url_to_redirect_target = models.URLField(blank=True, null=True)
  links_count = models.IntegerField()
  semantic_location = models.CharField(max_length=32, blank=True, null=True)
  page_title = models.CharField(max_length=255, blank=True, null=True)
  anchor_text = models.CharField(max_length=255, blank=True, null=True)
  alt_text = models.CharField(max_length=255, blank=True, null=True)
  backlink_spam_score = models.FloatField()
  item_type = models.CharField(max_length=32, blank=True, null=True)
  
  is_indirect_link = models.BooleanField()
  dofollow = models.BooleanField()
  is_broken = models.BooleanField()
  is_lost = models.BooleanField()
  is_new = models.BooleanField()

  first_seen = models.DateTimeField(blank=True, null=True)
  last_seen = models.DateTimeField(blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add=True)


  class Meta:
    db_table = 'backlinks'

  def __str__(self):
    return self.url_from


  def serialize(self):
    return {
      'id': self.id,
      'keyword': self.keyword.serialize(),
      'domain_from': self.domain_from,
      'domain_rank': self.domain_rank,
      'url_from': self.url_from,
      'url_to': self.url_to,
      'url_to_redirect_target': self.url_to_redirect_target,
      'links_count': self.links_count,
      'semantic_location': self.semantic_location,
      'page_title': self.page_title,
      'anchor_text': self.anchor_text,
      'alt_text': self.alt_text,
      'backlink_spam_score': self.backlink_spam_score,
      'item_type': self.item_type,
      'is_indirect_link': self.is_indirect_link,
      'dofollow': self.dofollow,
      'is_broken': self.is_broken,
      'is_lost': self.is_lost,
      'is_new': self.is_new,
      'first_seen': self.first_seen.isoformat(),
      'last_seen': self.last_seen.isoformat(),
      'created_at': self.created_at.isoformat(),
    }


class Content(models.Model):
  backlink = models.OneToOneField(Backlink, on_delete=models.CASCADE, related_name='content')

  topics = ArrayField(base_field=models.CharField(max_length=255), default=list, blank=True)
  title = models.CharField(max_length=255, blank=True, null=True)
  content_html = models.TextField(blank=True, null=True)
  anchor_text = models.CharField(max_length=255, blank=True, null=True)
  target_url = models.URLField(blank=True, null=True)
  author = models.CharField(max_length=255, blank=True, null=True)

  status = models.CharField(
    max_length=32,
    choices=[
      ('draft', 'Draft'),
      ('submitted', 'Submitted'),
      ('published', 'Published'),
      ('rejected', 'Rejected'),
    ],
    default='draft',
  )
  
  created_at = models.DateTimeField(auto_now_add=True)


  class Meta:
    db_table = 'contents'

  def __str__(self):
    return self.title
    