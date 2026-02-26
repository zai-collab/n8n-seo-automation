from django.db import models
from django.contrib.postgres.fields import ArrayField


class Metadata(models.Model):
  title = models.CharField(max_length=255)
  intent = models.CharField(max_length=255, blank=True)
  meta_description = models.TextField(blank=True)

  keyword = models.OneToOneField('kw.Keyword', on_delete=models.CASCADE, related_name='metadata')

  outline = models.JSONField(default=list, blank=True)

  must_cover = ArrayField(
    base_field=models.CharField(max_length=255),
    default=list,
    blank=True,
  )

  secondary_keywords = ArrayField(
    base_field=models.CharField(max_length=255),
    default=list,
    blank=True,
  )

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'metadata'

  def __str__(self):
    return self.title
