from django.contrib import admin

from .models import Keyword


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
  list_display = ('seed_keyword', 'keyword', 'search_volume', 'cpc', 'competition', 'keyword_difficulty', 'search_intent', 'created_at')
  search_fields = ('seed_keyword', 'keyword',)
  list_filter = ('created_at',)
