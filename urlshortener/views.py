from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UrlMapping
from .services import get_or_generate_short_url
from .serializers import UrlMappingInputSerializer, UrlMappingOutputSerializer


class ShortenUrlView(generics.GenericAPIView):
    serializer_class = UrlMappingInputSerializer

    # View to generate or fetch a shortened url. Takes Original URL as input.
    def post(self, request):
        input_serializer = UrlMappingInputSerializer(data=request.data)
        if input_serializer.is_valid():
            original_url = input_serializer.validated_data["original_url"]
            url_mapping = get_or_generate_short_url(original_url)

            output_serializer = UrlMappingOutputSerializer(
                url_mapping,
                context={"request": request}
            )
            return Response(output_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LookupUrlView(APIView):
    # View to fetch original url, takes short url as input.
    def get(self, request, short_url):
        try:
            url_mapping = UrlMapping.objects.get(short_url=short_url)

            serializer = UrlMappingOutputSerializer(
                url_mapping,
                context={"request": request}
            )
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        except UrlMapping.DoesNotExist:
            return Response(
                {"error": "Shortened Url not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class URLRedirectView(APIView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, short_url):
        # View to redirect a shortened URL to the original destination.
        # Increments click counter
        try:
            url_mapping = UrlMapping.objects.get(short_url=short_url)
            url_mapping.click_count += 1
            url_mapping.save()
            return redirect(url_mapping.original_url)
        except UrlMapping.DoesNotExist:
            # Redirect easter egg, in production a real 404 page would be implemented.
            return redirect("https://en.wikipedia.org/wiki/HTTP_404")
