from django.urls import path
from .api_views import (
    AdListAPIView, AdDetailAPIView, AdCreateAPIView, AdUpdateAPIView, AdDeleteAPIView,
    ProfileAdsAPIView, AdSearchAPIView, ExchangeListAPIView, ExchangeCreateAPIView
)
from .urls import app_name

app_name = "api"

urlpatterns = [
    path("", AdListAPIView.as_view(), name="ad- list"),
    path("<int:pk>/", AdDetailAPIView.as_view(), name="ad-detail"),
    path("create/", AdCreateAPIView.as_view(), name="ad-create"),
    path("update/<int:pk>/", AdUpdateAPIView.as_view(), name="ad-update"),
    path("delete/<int:pk>/", AdDeleteAPIView.as_view(), name="ad-delete"),
    path("profile/", ProfileAdsAPIView.as_view(), name="profile"),
    path("search/", AdSearchAPIView.as_view(), name="ad-search"),
    path("exchange/", ExchangeListAPIView.as_view(), name="exchange-list"),
    path("exchange/create/<int:pk>/", ExchangeCreateAPIView.as_view(), name="exchange-create"),
]
