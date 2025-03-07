from django.contrib import admin
from .models import UrlMapping


# Configure admin interface for the URL Mapping model.
class UrlAdmin(admin.ModelAdmin):
    fields = ["original_url", "short_url", "click_count", "created_at"]
    date_hierarchy = "created_at"


admin.site.register(UrlMapping, UrlAdmin)