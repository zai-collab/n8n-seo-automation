from django.contrib import admin

from .models import Metadata


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
  list_display = ('title', 'intent', 'meta_description', 'created_at')
  search_fields = ('title', 'intent', 'meta_description')
  list_filter = ('created_at',)