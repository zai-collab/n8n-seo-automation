from django.contrib import admin

from .models import Backlink


@admin.register(Backlink)
class BacklinkAdmin(admin.ModelAdmin):
  list_display = ('domain_from', 'domain_rank', 'url_from', 'url_to', 'links_count', 'semantic_location', 'anchor_text', 'alt_text', 'backlink_spam_score', 'dofollow', 'first_seen', 'last_seen', 'created_at')
  search_fields = ('domain_from', 'url_from', 'semantic_location', 'anchor_text', 'alt_text',)
  list_filter = ('created_at',)
