from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "ads"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/create/", views.AdCreateView.as_view(), name="create"),
    path("profile/detail/<int:pk>", views.AdDetailView.as_view(), name="detail"),
    path("profile/update/<int:pk>", views.AdUpdateView.as_view(), name="update"),
    path("profile/delete/<int:pk>", views.delete_ad, name="delete"),

]
