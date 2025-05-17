from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("detail/<int:pk>/", views.AdDetailView.as_view(), name="detail"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/create/", views.AdCreateView.as_view(), name="create"),
    path(
        "profile/update/<int:pk>/", views.AdUpdateView.as_view(),
        name="update"
    ),
    path("profile/delete/<int:pk>/", views.delete_ad, name="delete"),
    path(
        "profile/exchange/", views.ExchangeListView.as_view(),
        name="list_ex"
    ),
    path(
        "profile/exchange/ex_filter/<str:ex_filter>/",
        views.ExchangeListView.as_view(), name="ex_filter"
    ),
    path("searching/", views.SearchingView.as_view(), name="searching"),
    path(
        "filtering/<str:filtering>/", views.HomeView.as_view(),
        name="filtering"
    ),
    path("exchange/<int:pk>/", views.exchange_view, name="exchange"),

]
