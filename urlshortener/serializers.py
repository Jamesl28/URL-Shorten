from rest_framework import serializers
from .models import UrlMapping


# Simple Input serializer to valid the url user input.
class UrlMappingInputSerializer(serializers.Serializer):
    original_url = serializers.URLField(required=True)


# Output serializer which also builds the url using the current domain.
class UrlMappingOutputSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = UrlMapping
        fields = ["original_url", "short_url", "click_count"]

    def get_short_url(self, url_mapping):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/{url_mapping.short_url}/")
