from django.urls import path
from . import api_view

urlpatterns = [
    path("ad_list/", api_view.AdListApiView.as_view()),
    path("ex_list/", api_view.ExchangeListApiView.as_view()),
]