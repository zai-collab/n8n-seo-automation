from django.db import models


class Keyword(models.Model):
  seed_keyword = models.CharField(max_length=255, db_index=True)
  keyword = models.CharField(max_length=255, db_index=True)
  search_volume = models.IntegerField(db_index=True)
  cpc = models.FloatField(max_length=16, db_index=True)
  competition = models.FloatField(max_length=16, db_index=True)
  keyword_difficulty = models.FloatField(max_length=16, db_index=True)
  search_intent = models.CharField(max_length=32, db_index=True)

  status = models.CharField(
    max_length=32,
    choices=[
      ('pending', 'Pending'),
      ('approved', 'Approved'),
      ('analyzed', 'Analyzed'),
      ('rejected', 'Rejected'),
    ],
    default='pending',
  )

  created_at = models.DateTimeField(auto_now_add=True)


  class Meta:
    db_table = 'keywords'


  def __str__(self):
    return self.keyword


  def serialize(self):
    return {
      "id": self.id,
      "seed_keyword": self.seed_keyword,
      "keyword": self.keyword,
      "search_volume": self.search_volume,
      "cpc": self.cpc,
      "competition": self.competition,
      "keyword_difficulty": self.keyword_difficulty,
      "search_intent": self.search_intent,
      "status": self.status,
      "created_at": self.created_at.isoformat(),
    }
    