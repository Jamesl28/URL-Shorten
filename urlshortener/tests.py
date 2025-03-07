from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

from .models import UrlMapping
from .services import generate_short_url, get_or_generate_short_url
from .serializers import UrlMappingInputSerializer, UrlMappingOutputSerializer


class TestUrlMappingModel(TransactionTestCase):
    def test_url_mapping_create(self):
        # Test url model creation
        test_map = UrlMapping.objects.create(
            original_url="https://www.test.com",
            short_url="test123"
        )
        self.assertEqual(test_map.original_url, "https://www.test.com")
        self.assertEqual(test_map.short_url, "test123")
        self.assertEqual(test_map.click_count, 0)
        self.assertIsNotNone(test_map.created_at)

    def test_url_mapping_click_update(self):
        # Test click count update

        test_map = UrlMapping.objects.create(
            original_url="https://www.test.com",
            short_url="test123"
        )
        self.assertEqual(test_map.click_count, 0)
        test_map.click_count += 1
        test_map.save()

        updated_map = UrlMapping.objects.get(short_url="test123")
        self.assertEqual(updated_map.click_count, 1)


class TestUrlShortenService(TransactionTestCase):
    def test_generate_url(self):
        # Test Short URL generation and consistency
        original_url = "https://www.testmapping.com/index"
        first_short_url = generate_short_url(original_url)

        self.assertEqual(len(first_short_url), 7)

        second_short_url = generate_short_url(original_url)
        self.assertEqual(len(second_short_url), 7)
        self.assertEqual(first_short_url, second_short_url)

        new_url = "https://www.abc.com/def"
        new_short_url = generate_short_url(new_url)

        self.assertEqual(len(new_short_url), 7)
        self.assertNotEqual(first_short_url, new_short_url)

    def test_collision_handling(self):
        # Test collision handling by inserting a mapping with a known short URL
        original_url1 = "https://www.testmapping.com/"
        expected_short = generate_short_url(original_url1)

        # Create a URL mapping with the expected short URL
        UrlMapping.objects.create(
            original_url="https://www.testcollision.com/",
            short_url=expected_short
        )

        url_mapping = get_or_generate_short_url(original_url1)

        self.assertNotEqual(url_mapping.short_url, expected_short)
        self.assertEqual(len(url_mapping.short_url), len(expected_short) + 1)

        self.assertEqual(UrlMapping.objects.count(), 2)

    def test_get_or_generate_url(self):
        # Test Get function of get_or_generate function
        original_url = "https://www.testmapping.com/index"
        self.assertEqual(UrlMapping.objects.count(), 0)
        # Creating a new mapping object as url doesn't exist
        test_map = get_or_generate_short_url(original_url)
        self.assertEqual(len(test_map.short_url), 7)
        self.assertEqual(test_map.original_url, original_url)
        self.assertEqual(UrlMapping.objects.count(), 1)
        # Verify same mapping is returned
        test_get_map = get_or_generate_short_url(original_url)
        self.assertEqual(UrlMapping.objects.count(), 1)
        self.assertEqual(test_map.short_url, test_get_map.short_url)
        self.assertEqual(test_get_map.original_url, original_url)


class TestUrlShortenAPIViews(TransactionTestCase):
    def setUp(self):
        # Preparing client and URL mapping
        self.client = APIClient()
        self.shorten_url = reverse("shorten-url")

        self.url_mapping = UrlMapping.objects.create(
            original_url="https://www.test.com",
            short_url="miniurl"
        )

    def test_shorten_url_view(self):
        # Testing Shorten URL functionality
        # Valid URL
        data = {"original_url": "https://www.wikipedia.org"}
        response = self.client.post(self.shorten_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)
        self.assertEqual(UrlMapping.objects.count(), 2)

        # Invalid URL
        data = {"original_url": "I'm-not-a-valid-url"}
        response = self.client.post(self.shorten_url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(UrlMapping.objects.count(), 2)

    def test_lookup_url_view(self):
        # Testing Lookup URL Functionality
        # Existing short URL
        lookup_url = reverse("lookup-url", kwargs={"short_url": "miniurl"})
        response = self.client.get(lookup_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("short_url", response.data)

        # Nonexistent short url
        lookup_url = reverse("lookup-url", kwargs={"short_url": "badurl"})
        response = self.client.get(lookup_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirect_view(self):
        # Testing Redirect
        redirect_url = reverse("redirect-url", kwargs={"short_url": "miniurl"})
        response = self.client.get(redirect_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.url_mapping.original_url)

        mapping = UrlMapping.objects.get(short_url="miniurl")
        self.assertEqual(mapping.click_count, 1)

        redirect_url = reverse("redirect-url", kwargs={"short_url": "badurl"})
        response = self.client.get(redirect_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "https://en.wikipedia.org/wiki/HTTP_404")


class TestSerializers(TransactionTestCase):
    def test_input_serializer(self):
        # Testing Input Serializer validation
        # Valid
        serializer = UrlMappingInputSerializer(data={"original_url": "https://www.test.com"})
        self.assertTrue(serializer.is_valid())
        # Invalid
        serializer = UrlMappingInputSerializer(data={"original_url": "badurl"})
        self.assertFalse(serializer.is_valid())

    def test_output_serializer(self):
        # Testing Output Serializer validation
        url_mapping = UrlMapping.objects.create(
            original_url="https://www.test.com",
            short_url="miniurl",
            click_count=2
        )
        # Mocking the request
        factory = APIRequestFactory()
        request = factory.get('/')
        serializer = UrlMappingOutputSerializer(
            url_mapping,
            context={"request": request})
        data = serializer.data

        self.assertEqual(data["original_url"], "https://www.test.com")
        self.assertEqual(data["click_count"], 2)
        self.assertTrue(data["short_url"].endswith("/miniurl/"))
