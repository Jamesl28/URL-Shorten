from django.urls import path
from . import views

urlpatterns = [
    path("api/shorten/", views.ShortenUrlView.as_view(), name="shorten-url"),
    path("api/lookup/<str:short_url>/", views.LookupUrlView.as_view(), name="lookup-url"),
    path("<str:short_url>/", views.URLRedirectView.as_view(), name="redirect-url"),
]

