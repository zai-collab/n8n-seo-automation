from django.db import models


class Cluster(models.Model):
  name = models.CharField(max_length=255, db_index=True)
  intent = models.CharField(max_length=32, db_index=True)
  seed_keyword = models.CharField(max_length=255, db_index=True)

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'clusters'

  def __str__(self):
    return self.name


class Keyword(models.Model):
  cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name="keywords")

  keyword = models.CharField(max_length=255, db_index=True)
  search_volume = models.IntegerField()
  cpc = models.DecimalField(max_digits=10, decimal_places=2)
  competition = models.CharField(max_length=16, db_index=True)

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'keywords'

  def __str__(self):
    return self.keyword