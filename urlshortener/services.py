import hashlib
import base64
from .models import UrlMapping


def generate_short_url(url, length=7):
    # Create a hash of the url
    hash_obj = hashlib.md5(url.encode())
    hash_digest = hash_obj.digest()
    # Convert hash digest to base64 string
    short_url = base64.urlsafe_b64encode(hash_digest).decode("utf-8")
    short_url = "".join(c for c in short_url if c.isalnum())
    # return the url truncated to the "short" size
    # default length is 7 but increments in the case of collision
    return short_url[:length]


def get_or_generate_short_url(original_url):
    # First check if the url has already been shortened
    try:
        short_url = UrlMapping.objects.get(original_url=original_url)
        return short_url
    # If not, generate a new short url.
    # Collision is handled by checking if the resultant short string already exists
    # If so, increase the length and attempt again.
    except UrlMapping.DoesNotExist:
        short_url = generate_short_url(original_url)
        while UrlMapping.objects.filter(short_url=short_url).exists():
            short_url = generate_short_url(original_url, len(short_url) + 1)
        mini_url_mapping = UrlMapping.objects.create(
                            original_url=original_url,
                            short_url=short_url
                            )

        return mini_url_mapping
