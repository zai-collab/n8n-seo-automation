from django.contrib import admin

from .models import Metadata, Blog


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
  list_display = ('title', 'intent', 'meta_description', 'created_at')
  search_fields = ('title', 'intent', 'meta_description')
  list_filter = ('created_at',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'created_at')
  search_fields = ('title',)
  list_filter = ('created_at',)