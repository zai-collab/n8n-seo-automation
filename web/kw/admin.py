from django.contrib import admin

from .models import Cluster, Keyword


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
  list_display = ('name', 'intent', 'seed_keyword', 'created_at')
  search_fields = ('name', 'intent', 'seed_keyword')
  list_filter = ('created_at',)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
  list_display = ('keyword', 'search_volume', 'cpc', 'competition', 'created_at')
  search_fields = ('keyword', 'search_volume', 'cpc', 'competition')
  list_filter = ('created_at',)
