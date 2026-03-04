from django.db import models


class Backlink(models.Model):
  domain_from = models.URLField(blank=True, null=True)
  domain_rank = models.IntegerField()
  url_from = models.URLField(blank=True, null=True)
  url_to = models.URLField(blank=True, null=True)
  url_to_redirect_target = models.URLField(blank=True, null=True)
  links_count = models.IntegerField()
  semantic_location = models.CharField(max_length=32, blank=True, null=True)
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
