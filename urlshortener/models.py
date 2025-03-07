from django.db import models


# A simple model to link the original url with the shortened version.
# Also keeps track of creation date and click count.
class UrlMapping(models.Model):
    original_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=10, unique=True)
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
